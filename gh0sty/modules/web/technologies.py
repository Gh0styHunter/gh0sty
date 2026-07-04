"""Web technology signatures list."""

SERVER_SIGNATURES = {
    "nginx": "Nginx",
    "apache": "Apache HTTP Server",
    "cloudflare": "Cloudflare CDN / WAF",
    "microsoft-iis": "Microsoft IIS",
    "gws": "Google Web Server",
}

HEADER_SIGNATURES = {"x-powered-by": {"php": "PHP", "asp.net": "ASP.NET", "express": "Express.js"}}

COOKIE_SIGNATURES = {
    "phpsessid": "PHP",
    "jsessionid": "Java/JSP",
    "asp.net_sessionid": "ASP.NET",
    "csrftoken": "Django",
    "wp-": "WordPress",
}
