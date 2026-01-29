import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("/result", "routes/result.tsx"),
    route("/analysis/:inn", "routes/analysis.tsx"),
] satisfies RouteConfig;
