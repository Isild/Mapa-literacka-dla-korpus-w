import Vue from "vue";
import Router from "vue-router";
import Home from "../pages/Home";
import LoadFile from "../pages/LoadFile";
import ForceGraph from "../components/ForceGraph";
import VisualiseData from "../components/VisualiseData";
import GraphList from "../pages/GraphList";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },

    {
      path: "/force-graph",
      name: "ForceGraph",
      component: ForceGraph
    },

    {
      path: "/visualise-data/:id",
      name: "VisualiseData",
      component: VisualiseData,
      props: true
    },
    {
      path: "/load-file",
      name: "LoadFile",
      component: LoadFile
    },
    {
      path: "/graph-list",
      name: "GraphList",
      component: GraphList
    }
  ]
});
