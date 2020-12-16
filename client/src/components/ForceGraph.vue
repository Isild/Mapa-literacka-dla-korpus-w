<template>
  <v-row align="center" justify="center">
    <div
      :style="{
        width: width + 'px',
        height: height + 'px',
        border: '2px solid blue'
      }"
    >
      <svg width="100%" height="100%" id="forceGraph-svg">
        <defs>
          <pattern
            id="innerGrid"
            :width="innerGridSize"
            :height="innerGridSize"
            patternUnits="userSpaceOnUse"
          >
            <rect
              width="100%"
              height="100%"
              fill="none"
              stroke="#CCCCCC7A"
              stroke-width="0.5"
            />
          </pattern>
          <pattern
            id="grid"
            :width="gridSize"
            :height="gridSize"
            patternUnits="userSpaceOnUse"
          >
            <rect
              width="100%"
              height="100%"
              fill="url(#innerGrid)"
              stroke="#CCCCCC7A"
              stroke-width="1.5"
            />
          </pattern>
        </defs>
      </svg>
    </div>
  </v-row> </template
>>

<script>
import * as d3 from "d3";
import removedNodeTag from "../plugins/const";

export default {
  props: [
    "data",
    "nodeNameA",
    "nodeNameB",
    "forceSwitch",
    "forceSlider",
    "alphaSwitch"
  ],
  data() {
    return {
      width: 1500,
      height: 768,
      gridSize: 100,
      selections: {},
      simulation: null,
      forceProperties: {
        center: {
          x: 0.5,
          y: 0.5
        },
        charge: {
          enabled: true,
          strength: -2000, // could be controlled by slider
          distanceMin: 1,
          distanceMax: 2000
        },
        collide: {
          enabled: true,
          strength: 0.7,
          iterations: 1,
          radius: 35
        },
        forceX: {
          enabled: true,
          strength: 0.03,
          x: 0.5
        },
        forceY: {
          enabled: true,
          strength: 0.03,
          y: 0.5
        },
        link: {
          enabled: true,
          distance: 100,
          iterations: 1
        }
      }
    };
  },
  computed: {
    innerGridSize() {
      return this.gridSize / 10;
    },
    nodes() {
      return this.data.nodes;
    },
    links() {
      return this.data.links;
    }
  },
  created() {
    this.width = window.innerWidth - 500;
    this.height = window.innerHeight - 300;

    this.simulation = d3
      .forceSimulation()
      .force("link", d3.forceLink())
      .force("charge", d3.forceManyBody())
      .force("collide", d3.forceCollide())
      .force("center", d3.forceCenter())
      .force("forceX", d3.forceX())
      .force("forceY", d3.forceY())
      .on("tick", this.tick);
    this.updateForces();
  },
  mounted() {
    this.selections.svg = d3.select(this.$el.querySelector("svg"));
    const svg = this.selections.svg;

    // Add zoom and panning triggers
    this.zoom = d3
      .zoom()
      .scaleExtent([1 / 12, 4])
      .on("zoom", this.zoomed);
    svg.call(this.zoom);

    // Background grid
    // The width and height depends on the minimum scale extent and
    // the + 10% and negative index to create an infinite grid feel
    this.selections.grid = svg
      .append("rect")
      .attr("x", "-10%")
      .attr("y", "-10%")
      .attr("width", "410%")
      .attr("height", "410%")
      .attr("fill", "url(#grid)");

    this.selections.graph = svg.append("g");

    // Node and link count
    this.selections.statsNodes = svg
      .append("text")
      .attr("x", "1%")
      .attr("y", "96%")
      .attr("text-anchor", "left");

    this.selections.statsConnections = svg
      .append("text")
      .attr("x", "1%")
      .attr("y", "98%")
      .attr("text-anchor", "left");
  },
  methods: {
    nodeColor(percent) {
      return (
        "#" +
        (
          (1 << 24) +
          ((255 - Math.floor((percent / 100.0) * 255.0)) << 16) +
          ((255 - Math.floor((136 * percent) / 100)) << 8) +
          255
        )
          .toString(16)
          .slice(1)
      );
    },
    tick() {
      // If no data is passed to the Vue component, do nothing
      if (!this.data) {
        return;
      }
      const transform = d => {
        return "translate(" + d.x + "," + d.y + ")";
      };

      const link = d => {
        return (
          "M" +
          d.source.x +
          "," +
          d.source.y +
          " L" +
          d.target.x +
          "," +
          d.target.y
        );
      };

      const graph = this.selections.graph;
      graph.selectAll("path").attr("d", link);
      graph.selectAll("circle").attr("transform", transform);
      graph.selectAll("text").attr("transform", transform);

      this.updateNodeLinkCount();
    },
    highlightToBeMerged() {
      const graph = this.selections.graph;
      // Clear all highlights
      graph.selectAll("circle").attr("class", "circle");

      if (this.nodeNameA !== null) {
        graph
          .selectAll("circle")
          .filter(d => {
            return d.name === this.nodeNameA;
          })
          .attr("class", "redd");
      }

      if (this.nodeNameB !== null) {
        graph
          .selectAll("circle")
          .filter(d => {
            return d.name === this.nodeNameB;
          })
          .attr("class", "greenn");
      }
    },
    updateData() {
      this.simulation.nodes(this.nodes);
      this.simulation.force("link").links(this.links);

      const simulation = this.simulation;
      const graph = this.selections.graph;

      graph.selectAll("path").remove();
      graph
        .selectAll("path")
        .data(this.links)
        .enter()
        .append("path")
        .attr("stroke", d => this.nodeColor(Math.max(15, d.value)))
        .attr("stroke-width", d => Math.max(1, Math.sqrt(d.value / 4)));

      // Redrawing nodes to avoid lines above them
      graph.selectAll("circle").remove();
      graph
        .selectAll("circle")
        .data(this.nodes)
        .enter()
        .append("circle")
        .attr("r", 30)
        .attr("class", "circle")
        .attr("fill", d =>
          this.nodeColor(Math.max(10, Math.min(100, d.occurrence)))
        )
        .call(
          d3
            .drag()
            .on("start", this.nodeDragStarted)
            .on("drag", this.nodeDragged)
            .on("end", this.nodeDragEnded)
        )
        .on("mouseover", this.nodeMouseOver)
        .on("mouseout", this.nodeMouseOut)
        .on("click", this.nodeClick);

      graph.selectAll("text").remove();
      graph
        .selectAll("text")
        .data(this.nodes)
        .enter()
        .append("text")
        .attr("x", 0)
        .attr("y", ".31em")
        .attr("text-anchor", "middle")
        .text(d => d.name);

      // Deleting merged nodes
      graph
        .selectAll("circle")
        .data(this.nodes)
        .filter(function(d) {
          return d.name === removedNodeTag;
        })
        .remove();

      graph
        .selectAll("text")
        .data(this.nodes)
        .filter(function(d) {
          return d.name === removedNodeTag;
        })
        .remove();
      simulation.alpha(1).restart();
    },
    updateForces() {
      const { simulation, forceProperties, width, height } = this;
      if (!this.forceSwitch) {
        simulation.stop();
        return;
      }
      simulation
        .force("center")
        .x(width * forceProperties.center.x)
        .y(height * forceProperties.center.y);
      simulation
        .force("charge")
        .strength(
          forceProperties.charge.strength * forceProperties.charge.enabled
        )
        .distanceMin(forceProperties.charge.distanceMin)
        .distanceMax(forceProperties.charge.distanceMax);
      simulation
        .force("collide")
        .strength(
          forceProperties.collide.strength * forceProperties.collide.enabled
        )
        .radius(forceProperties.collide.radius)
        .iterations(forceProperties.collide.iterations);
      simulation
        .force("forceX")
        .strength(
          forceProperties.forceX.strength * forceProperties.forceX.enabled
        )
        .x(width * forceProperties.forceX.x);
      simulation
        .force("forceY")
        .strength(
          forceProperties.forceY.strength * forceProperties.forceY.enabled
        )
        .y(height * forceProperties.forceY.y);
      simulation
        .force("link")
        .distance(forceProperties.link.distance)
        .iterations(forceProperties.link.iterations);
      simulation.velocityDecay((100 - this.forceSlider) / 100);
      simulation.alphaDecay(0.0228);
      simulation.alphaTarget(0.05 + this.alphaSwitch * 0.4);
      simulation.alpha(1).restart();
    },
    updateNodeLinkCount() {
      let nodeCount = this.nodes.length;
      let linkCount = this.links.length;

      const highlightedNodes = this.selections.graph.selectAll(
        "circle.highlight"
      );
      const highlightedLinks = this.selections.graph.selectAll(
        "path.highlight"
      );
      if (highlightedNodes.size() > 0 || highlightedLinks.size() > 0) {
        nodeCount = highlightedNodes.size();
        linkCount = highlightedLinks.size();
      }
      this.selections.statsNodes.text("Nodes: " + nodeCount);
      this.selections.statsConnections.text("Connections: " + linkCount);
    },
    zoomed() {
      const transform = d3.event.transform;
      // The trick here is to move the grid in a way that the user doesn't perceive
      // that the axis aren't really moving
      // The actual movement is between 0 and gridSize only for x and y
      const translate =
        (transform.x % (this.gridSize * transform.k)) +
        "," +
        (transform.y % (this.gridSize * transform.k));
      this.selections.grid.attr(
        "transform",
        "translate(" + translate + ") scale(" + transform.k + ")"
      );
      this.selections.graph.attr("transform", transform);
    },
    nodeDragStarted(d) {
      if (!d3.event.active) {
        // this.simulation.alphaTarget(0.3).restart();
      }
      d.fx = d.x;
      d.fy = d.y;
    },
    nodeDragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
      if (!this.forceSwitch) {
        this.simulation.velocityDecay(1);
        this.simulation.alphaDecay(0.0001).restart();
      } else {
        this.simulation.alphaTarget(0.3).restart();
      }
    },
    nodeDragEnded(d) {
      if (!d3.event.active) {
        this.simulation.alphaTarget(0.05 + this.alphaSwitch * 0.4);
      }
      d.fx = null;
      d.fy = null;
      if (!this.forceSwitch) {
        this.simulation.stop();
      }
    },
    nodeMouseOver(d) {
      const graph = this.selections.graph;
      const circle = graph.selectAll("circle");
      const path = graph.selectAll("path");
      const text = graph.selectAll("text");

      const related = [];
      const relatedLinks = [];
      related.push(d);
      this.simulation
        .force("link")
        .links()
        .forEach(link => {
          if (link.source === d || link.target === d) {
            relatedLinks.push(link);
            if (related.indexOf(link.source) === -1) {
              related.push(link.source);
            }
            if (related.indexOf(link.target) === -1) {
              related.push(link.target);
            }
          }
        });
      circle.classed("faded", true);
      circle.filter(df => related.indexOf(df) > -1).classed("highlight", true);
      path.classed("faded", true);
      path
        .filter(df => df.source === d || df.target === d)
        .classed("highlight", true);
      text.classed("faded", true);
      text.filter(df => related.indexOf(df) > -1).classed("highlight", true);
      // This ensures that tick is called so the node count is updated
      // this.simulation.alphaTarget(0.0001).restart();
    },
    nodeMouseOut() {
      const graph = this.selections.graph;
      const circle = graph.selectAll("circle");
      const path = graph.selectAll("path");
      const text = graph.selectAll("text");

      circle.classed("faded", false);
      circle.classed("highlight", false);
      path.classed("faded", false);
      path.classed("highlight", false);
      text.classed("faded", false);
      text.classed("highlight", false);
      // This ensures that tick is called so the node count is updated
      // this.simulation.restart();
    },
    nodeClick(d) {
      const circle = this.selections.graph.selectAll("circle");
      circle.classed("selected", false);
      circle.filter(td => td === d).classed("selected", true);
    }
  },
  watch: {
    data: {
      handler() {
        this.updateData();
      },
      deep: true
    },
    forceProperties: {
      handler() {
        this.updateForces();
      },
      deep: true
    },
    alphaSwitch: {
      handler() {
        this.updateForces();
      },
      deep: true
    },
    forceSwitch: {
      handler() {
        this.updateForces();
      },
      deep: true
    },
    forceSlider: {
      handler() {
        this.updateForces();
      },
      deep: true
    },
    nodeNameA: {
      handler() {
        this.highlightToBeMerged();
      },
      deep: true
    },
    nodeNameB: {
      handler() {
        this.highlightToBeMerged();
      },
      deep: true
    }
  }
};
</script>
>

<style>
#forceGraph-svg .faded {
  opacity: 0.1;
  transition: 0.2s opacity;
}
#forceGraph-svg .highlight {
  opacity: 1;
}

#forceGraph-svg circle {
  stroke: black;
  stroke-width: 1.5px;
}

#forceGraph-svg circle.redd {
  fill: red;
  stroke: #001900;
  animation: red-animation 0.5s 2 alternate ease-in-out;
}

#forceGraph-svg circle.greenn {
  fill: green;
  stroke: #001900;
  animation: green-animation 0.5s 2 alternate ease-in-out;
}

#forceGraph-svg circle.selected {
  stroke: rgb(0, 0, 0);
  stroke-width: 1px;
  animation: selected 0.5s 4 alternate ease-in-out;
}

@keyframes selected {
  from {
    stroke-width: 1px;
    r: 30;
  }
  to {
    stroke-width: 5px;
    r: 31;
  }
}
@keyframes red-animation {
  from {
    stroke-width: 1px;
    stroke: black;
    r: 30;
  }
  to {
    stroke-width: 4px;
    stroke: red;
    r: 32;
  }
}
@keyframes green-animation {
  from {
    stroke-width: 1px;
    stroke: black;
    r: 30;
  }
  to {
    stroke-width: 4px;
    stroke: green;
    r: 32;
  }
}
#forceGraph-svg text {
  font: 10px arial;
  pointer-events: none;
  text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;
}
</style>
