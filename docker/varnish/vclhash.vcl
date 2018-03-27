# Put the output of `python manage.py generate_vcl` here.


sub vcl_hash {
    # Cache even with cookies present. Note we don't delete the cookies. Also,
    # we only consider cookies listed in the Hash-Cookies variable as part
    # of the hash. This list is determined by the relevant Django Cache Headers
    # policy.
if (req.url ~ "^/anonymous-and-authenticated/") {
set req.http.Hash-Cookies = "messages|isauthenticated";
}
else if (req.url ~ "^/anonymous-only/") {
set req.http.Hash-Cookies = "messages|isauthenticated";
}
else if (req.url ~ "^/all-users/") {
set req.http.Hash-Cookies = "messages";
}
else if (req.url ~ "^/per-user/") {
set req.http.Hash-Cookies = "messages|sessionid";
}

    set req.http.Hash-Value = "x";
    if (req.http.Hash-Cookies) {
        # todo: softcode these checks
        if (req.http.Hash-Cookies ~ "messages") {
            if (req.http.Cookie ~ "messages=") {
                set req.http.Hash-Value = req.http.Hash-Value + regsub(req.http.Cookie, ".*messages=([^;]+).*", "\1");
            }
        }
        if (req.http.Hash-Cookies == "messages|isauthenticated") {
            if (req.http.Cookie ~ "isauthenticated=1") {
                set req.http.Hash-Value = req.http.Hash-Value + "1";
            }
        }
        else if (req.http.Hash-Cookies == "messages|sessionid") {
            if (req.http.Cookie ~ "sessionid=") {
                set req.http.Hash-Value = req.http.Hash-Value + regsub(req.http.Cookie, ".*sessionid=([^;]+).*", "\1");
            }
        }
    }   

    hash_data(req.http.Hash-Value);

    unset req.http.Hash-Cookies;
    unset req.http.Hash-Value;
}
