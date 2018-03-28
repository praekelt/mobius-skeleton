# Use 4.0 format
vcl 4.0;
import directors;
import dynamic;

# Backends
backend default {
    .host = "localhost";
    .port = "8000";
}

# Access control
acl purge {
    "localhost";
    "127.0.0.1";
}

# Load balancer
probe myprobe {
    .url = "/mobius/health/";
    .window = 5;
    .threshold = 3;
    .interval = 5s;
    .initial = 10;
    .timeout = 1s;
}

sub vcl_init {
    new app_director = dynamic.director(
        port = "80",
        share = HOST,
        probe = myprobe,
        ttl = 1m
    );
    new daphne_director = dynamic.director(
        port = "80",
        share = HOST,
        probe = myprobe,
        ttl = 1m
    );
}

# vcl_recv adapted from the Varnish default
sub vcl_recv {
    if (req.method == "PURGE") {
        if (!client.ip ~ purge) {
            return(synth(405, "Not allowed."));
        }
        return(purge);
    }
    if (req.http.upgrade ~ "(?i)websocket") {
        set req.backend_hint = daphne_director.backend("daphne");
        return (pipe);
    }
    set req.backend_hint = app_director.backend("app");
    if (req.method == "PRI") {
        # We do not support SPDY or HTTP/2.0
        return(synth(405));
    }
    if (req.method != "GET" &&
      req.method != "HEAD" &&
      req.method != "PUT" &&
      req.method != "POST" &&
      req.method != "TRACE" &&
      req.method != "OPTIONS" &&
      req.method != "DELETE") {
        # Non-RFC2616 or CONNECT which is weird
        return(pipe);
    }
    if (req.method != "GET" && req.method != "HEAD") {
        # We only deal with GET and HEAD by default
        return(pass);
    }
    if (req.http.Authorization) {
        # Not cacheable by default
        return(pass);
    }
    return(hash);
}

sub vcl_pipe {
    if (req.http.upgrade) {
        set bereq.http.upgrade = req.http.upgrade;
        set bereq.http.connection = req.http.connection;
    }
}

sub vcl_backend_response {
    # Make no assumptions about the state of Vary before hand. All that is
    # needed is to temporarily remove Cookie from the Vary header while it
    # gets passed through the rest of the varnish functions.
    set beresp.http.Original-Vary = beresp.http.Vary;
    set beresp.http.Vary = regsub(beresp.http.Vary, "Cookie", "Substitute");
    set beresp.http.X-Backend-IP = beresp.backend.ip;
}

sub vcl_deliver {
    if (obj.hits > 0) {
        set resp.http.X-Cache = "HIT";
    } else {
        set resp.http.X-Cache = "MISS";
    }

    # Replace the original Vary header on the response
    set resp.http.Vary = resp.http.Original-Vary;

    # Unset the backup just in case
    unset resp.http.Original-Vary;
}

include "/etc/varnish/vclhash.vcl";
