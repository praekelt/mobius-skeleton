// #############
// SETUP

const BASE_PROJECT_NAME = 'skeleton';
const PACKAGE_JSON = require('./package.json');

const
    Path = require('path'),

    // Custom Helpers
    Helpers = require('./build-helpers/webpack/helpers'),

    // Webpack Utils
    Merge = require('webpack-merge'),

    // Grab dependencies dict from package.json
    VendorDependencies = Object.keys(PACKAGE_JSON.dependencies) || [];

// Set environment variables
const LifecycleEvent = process.env.npm_lifecycle_event;
const Argv = require('yargs')
    .default('projectName', BASE_PROJECT_NAME)
    .default('projectAspect', 'website')
    .argv;

const MotePath = `/mote/projects/${Argv.projectName}/${Argv.projectAspect}`;
const PublicStaticPath = `/static/${BASE_PROJECT_NAME === Argv.projectName ? BASE_PROJECT_NAME : BASE_PROJECT_NAME + '/' + Argv.projectName}/generated_statics/bundles/`;

const ProjectPaths = {
    root: Path.join(__dirname, MotePath),
    src: Path.join(__dirname, MotePath + '/src'),
    dist: Path.join(__dirname, `${BASE_PROJECT_NAME}${PublicStaticPath}`)
};

function filenamePattern(prefix, ext) {
    return `${prefix}.[name].[chunkhash].${ext}`;
}

function bundlenamePattern(prefix) {
    return `./${prefix}-bundlemap.json`;
}



// #############
// WEBPACK BUILD

const BASE_CONFIG = {
    entry: {
        main: ProjectPaths.src + '/main.js'
    },
    output: {
        path: ProjectPaths.dist,
        filename: filenamePattern(`${Argv.projectName}-${Argv.projectAspect}`, 'js'),
        publicPath: PublicStaticPath
    },
    resolve: {
        extensions: [
            '.js',
            '.jsx',
            '.css',
            '.scss',
            '.sass',
            '.json'
        ],
        modules: [
            'node_modules',
            ProjectPaths.src + '/patterns'
        ]
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                enforce: 'pre',
                loader: 'eslint-loader',
                include: ProjectPaths.src
            }
        ]
    }
}

// Stitch together the correct config based on the environment.
function configBuilder(process, config, env) {
    let mergedConfig;

    switch (process) {
        // #################
        // Profile Build
        // TODO: refactor config to not tie build script name to exicution type any more.
        case 'build:profile':
        // ################
        // Production Build
        case 'build':
            mergedConfig = Merge(
                config,
                {
                    // Don't attempt to continue if there are any errors.
                    bail: true,
                    // We generate sourcemaps in production. This is slow but gives good results.
                    // You can exclude the *.map files from the build during deployment.
                    devtool: 'source-map',
                    entry: {
                        styles: Path.join(__dirname, MotePath + '/src', 'styles.scss')
                    },
                },
                Helpers.clean(ProjectPaths.dist),
                Helpers.setFreeVariable(
                    'process.env.NODE_ENV',
                    'production'
                ),
                Helpers.extractBundles([
                    {
                        name: 'vendor',
                        minChunks: ({resource}) => (
                            resource &&
                            resource.indexOf('node_modules') >= 0 &&
                            resource.match(/\.js$/)
                        )
                    },
                    {
                        name: 'manifest',
                        minChunks: Infinity
                    }
                ]),
                Helpers.setupJS(ProjectPaths.src),
                Helpers.lintCSS({
                    configFile: '.stylelintrc',
                    fileGlob: [
                        MotePath + '/src/*.s?(a|c)ss',
                        MotePath + '/src/+(helpers|patterns)/*.s?(a|c)ss'
                    ]
                }),
                Helpers.globSass(),
                Helpers.extractCSS({
                    filename: filenamePattern(`${Argv.projectName}-${Argv.projectAspect}`, 'css'),
                    include: [
                        Path.join(__dirname, MotePath + '/src/styles.scss')
                    ],
                    path: ProjectPaths.src
                }),
                Helpers.minify(),
                Helpers.trackBundles({
                    path: ProjectPaths.dist,
                    filename: bundlenamePattern(`${Argv.projectName}-${Argv.projectAspect}`)
                }),
                env ? Helpers.bundleAnalyzer(env) : {}
            );
            break;


        // #################
        // Development Build
        case 'build:dev':
            mergedConfig = Merge(
                config,
                {
                    // You may want 'eval' instead if you prefer to see the compiled output in DevTools.
                    // See the discussion in https://github.com/facebookincubator/create-react-app/issues/343.
                    devtool: 'cheap-module-source-map',
                    entry: [
                        'webpack-dev-server/client?http://localhost:3000',
                        'webpack/hot/only-dev-server',
                        ProjectPaths.src + '/main'
                    ],
                    output: {
                        filename: '[name].js',
                        chunkFilename: '[hash].js', // Used for require.ensure,
                        publicPath: 'http://localhost:3000' + PublicStaticPath
                    },
                },
                Helpers.dashboard(),
                Helpers.devServer({
                    publicPath: BASE_CONFIG.output.publicPath
                }),
                Helpers.setFreeVariable(
                    'process.env.NODE_ENV',
                    'development'
                ),
                Helpers.setupJS(ProjectPaths.src),
                Helpers.lintCSS({
                    configFile: '.stylelintrc',
                    fileGlob: [
                        MotePath + '/src/*.s?(a|c)ss',
                        MotePath + '/src/+(helpers|patterns)/*.s?(a|c)ss'
                    ]
                }),
                Helpers.globSass(),
                Helpers.setupCSS({
                    path: ProjectPaths.src,
                    include: [
                        Path.join(__dirname, MotePath + '/src', 'styles.scss')
                    ]
                }),
                Helpers.trackBundles({
                    path: ProjectPaths.dist,
                    filename: bundlenamePattern(`${Argv.projectName}-${Argv.projectAspect}`)
                })
            );
            break;
    }

    return mergedConfig;
}

//TODO: refactor once we have switched too useing --env for all flags instad of using lifecycleEvents.
module.exports = (env) =>  configBuilder(LifecycleEvent, BASE_CONFIG, env);
