<template>
  <v-container>
    <v-row>
      <v-col cols="12" align="center" v-show="isLoading">
        <v-progress-circular
          :indeterminate="true"
          :size="19"
          :width="3"
          style="margin-right: 5px;"
        ></v-progress-circular>
        Tekst jest analizowany. Wróć później.
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <ForceGraph
          :data="getDataFilteredBySensitivity"
          :nodeNameA="nodeNameA"
          :nodeNameB="nodeNameB"
          :forceSwitch="forceSwitch"
          :forceSlider="forceSlider"
          :alphaSwitch="alphaSwitch"
          ref="forceGraph"
        ></ForceGraph>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-row justify="center" align="center">
          <v-col cols="2">
            <v-switch v-model="forceSwitch" label="Symulacja"></v-switch>
          </v-col>
          <v-col cols="2">
            <v-switch
              v-model="alphaSwitch"
              :disabled="!forceSwitch"
              label="Przyspieszona Symulacja"
            ></v-switch>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-slider
              min="1"
              max="80"
              v-model="forceSlider"
              label="Sprężystość"
            />
          </v-col>
          <v-col>
            <v-slider
              min="0"
              :max="sliderMaxNodes"
              v-model="sliderNodes"
              label="Czułość wierzchołków"
            />
          </v-col>
          <v-col>
            <v-slider
              min="0"
              :max="sliderMaxEdges"
              v-model="sliderEdges"
              label="Czułość krawędzi"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="inputUrl"
              label="Link do testowania"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="3" class="text-center">
            <v-btn @click="loadJsonFromUrl()" small color="primary">
              Wczytaj dane z adresu
            </v-btn>
          </v-col>
          <v-col cols="3" class="text-center">
            <v-file-input label="Wybierz plik..." v-model="fileToUpload" />
            <v-btn @click="loadFromFile()" small color="primary">
              Wczytaj dane z pliku
            </v-btn>
          </v-col>
          <v-col cols="3" class="text-center">
            <v-btn @click="saveToFile()" small color="primary">
              Zapisz dane do pliku
            </v-btn>
          </v-col>
          <v-col cols="3" class="text-center">
            <v-btn @click="saveGraphToPng()" small color="primary">
              Zapisz graf do pliku graficznego
            </v-btn>
          </v-col>
        </v-row>
        <v-divider class="mx-4"></v-divider>
        <v-spacer></v-spacer>
        <v-row align="center" justify="center">
          <v-col cols="3"></v-col>
          <v-col cols="3">
            <v-autocomplete
              v-model="nodeNameA"
              :items="items"
              dense
              filled
              label="Byt (usuń)"
            ></v-autocomplete>
          </v-col>
          <v-col cols="3">
            <v-autocomplete
              v-model="nodeNameB"
              :items="items"
              dense
              filled
              label="Drugi byt (zachowaj)"
            ></v-autocomplete>
          </v-col>
          <v-col cols="1">
            <v-btn
              v-if="nodeNameA || nodeNameB"
              @click="clearMergeFields()"
              small
              dark
              color="primary"
              >Wyczyść
            </v-btn>
          </v-col>
          <v-col cols="2"></v-col>
        </v-row>
        <v-row>
          <v-col cols="3"></v-col>
          <v-col cols="3" class="text-center">
            <v-btn @click="mergeNodes()" small color="primary">
              Połącz byty
            </v-btn>
          </v-col>
          <v-col cols="3" class="text-center">
            <v-btn @click="restore()" small color="primary">
              Przywróć zmiany
            </v-btn>
          </v-col>
          <v-col cols="3"></v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-dialog v-model="isFileToUpload" max-width="300">
      <v-card color="warning">
        <v-card-title>Nie wybrałeś pliku!</v-card-title>

        <v-card-text>
          Aby załadować dane wybierz plik.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="isFileToUpload = false">
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="mergeError" max-width="400">
      <v-card color="warning">
        <v-card-title>
          Najpierw wpisz nazwy nazwy bytów!
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="mergeError = false">
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import ForceGraph from "./ForceGraph.vue";
import * as d3 from "d3";
import { saveAs } from "file-saver";
import { saveSvgAsPng } from "save-svg-as-png";
import removedNodeTag from "../plugins/const";
import axios from "axios";

export default {
  name: "VisualizeData",
  components: {
    ForceGraph
  },
  props: ["id"],
  data() {
    return {
      graphId: -1,
      sliderNodes: 100,
      sliderMaxNodes: 1,
      sliderEdges: 100,
      sliderMaxEdges: 1,
      alphaSwitch: false,
      forceSwitch: true,
      forceSlider: 80,
      nodeNameA: null,
      nodeNameB: null,
      mergeError: false,
      items: null,
      originalData: null, // Original data for json
      data: null, // Separate data structure for D3
      changedData: null, // Data to be worked with. Structure unchanged by d3
      inputUrl:
        "https://gist.githubusercontent.com/DawidPiechota/cd310d7f93c05a2dd5a164850a44a6f3/raw/e7f87b888f8e7ec92dfa00c7ed2d2909fc23d7a4/dataMiserables.json",
      fileToUpload: null,
      isFileToUpload: null,
      isLoading: true
    };
  },
  computed: {
    getDataFilteredBySensitivity() {
      const filteredData = {};
      filteredData.nodes = [];
      filteredData.links = [];
      if (
        this.changedData &&
        this.changedData.nodes &&
        this.changedData.links
      ) {
        this.data.nodes.forEach(item => {
          if (item.occurrence >= this.sliderMaxNodes - this.sliderNodes) {
            filteredData.nodes.push(item);
          }
        });
        this.data.links.forEach(item => {
          const linkItem = item;
          if (
            filteredData.nodes.some(item => {
              return item.index === linkItem.source.index;
            }) &&
            filteredData.nodes.some(item => {
              return item.index === linkItem.target.index;
            }) &&
            item.value >= this.sliderMaxEdges - this.sliderEdges
          ) {
            console.log(item);
            filteredData.links.push(item);
          }
        });
        return filteredData;
      }
      return this.data;
    }
  },
  mounted() {
    this.graphId = parseInt(this.$props.id, 10);
    if (this.graphId === 0) {
      this.loadJsonFromUrl();
      return;
    }
    this.loadJsonFromDb();
  },
  methods: {
    nodes() {
      this.items = this.changedData.nodes
        .filter(d => {
          if (d.name === removedNodeTag) {
            return false;
          }
          return true;
        })
        .map(d => d.name);
      return this.items;
    },
    mergeNodes() {
      if (!this.exists(this.nodeNameA, this.nodeNameB)) {
        this.mergeError = true;
        return;
      }
      for (let i = 0; i < this.changedData.nodes.length; i++) {
        if (this.changedData.nodes[i].name === this.nodeNameA) {
          for (let j = 0; j < this.changedData.nodes.length; j++) {
            if (this.changedData.nodes[j].name === this.nodeNameB) {
              const sum = Math.min(
                100,
                parseInt(this.changedData.nodes[i].occurrence) +
                  parseInt(this.changedData.nodes[j].occurrence)
              );
              this.changedData.nodes[j].occurrence = sum;
            }
          }
        }
      }
      const indexA = this.markNode(this.nodeNameA);
      const indexB = this.getIndexOfNode(this.nodeNameB);
      this.mergeLinks(indexA, indexB); // second one stays
      this.data = JSON.parse(JSON.stringify(this.changedData)); // update the data
      this.items = this.nodes();
      this.nodeNameA = null;
      this.nodeNameB = null;
    },
    mergeLinks(indexA, indexB) {
      for (let i = 0; i < this.changedData.links.length; i++) {
        let linkType = 0;
        if (this.changedData.links[i].source === indexA) {
          // source zgadza się z index A
          linkType += 1;
        }
        if (this.changedData.links[i].target === indexA) {
          // target zgadza się z index A
          linkType += 2;
        }

        switch (linkType) {
          case 1:
            this.changedData.links[i].source = indexB;
            break;
          case 2:
            this.changedData.links[i].target = indexB;
            break;
          case 3:
            break;
          default:
          // not possible
        }
      }
    },
    exists(nameA, nameB) {
      let occuranceCount = 0;
      for (let i = 0; i < this.changedData.nodes.length; i++) {
        if (
          this.changedData.nodes[i].name === nameA ||
          this.changedData.nodes[i].name === nameB
        ) {
          occuranceCount++;
        }
      }
      if (occuranceCount === 2) return true;
      else return false;
    },
    getIndexOfNode(name) {
      for (let i = 0; i < this.changedData.nodes.length; i++) {
        if (this.changedData.nodes[i].name === name) {
          return i;
        }
      }
    },
    markNode(name) {
      // returns node index
      for (let i = 0; i < this.changedData.nodes.length; i++) {
        if (this.changedData.nodes[i].name === name) {
          this.changedData.nodes[i].name = removedNodeTag;
          return i;
        }
      }
    },
    loadJsonFromUrl() {
      this.forceSwitch = true;
      // wrapper for fetch basically
      d3.json(this.inputUrl).then(data => {
        this.originalData = JSON.parse(JSON.stringify(data));
        this.changedData = JSON.parse(JSON.stringify(data)); // Hacky way to copy json
        this.data = JSON.parse(JSON.stringify(data));
        this.items = this.nodes();
        this.setMaxSensitivityValues();
        this.isLoading = false;
      });
    },
    loadJsonFromDb() {
      return axios
        .get("http://127.0.0.1:5000/methodOne?id=" + this.graphId, {
          headers: {
            "Content-type": "application/json"
          }
        })
        .then(response => {
          if (response.data.status === "ready") {
            // hacky way to deep copy arrays
            this.originalData = JSON.parse(
              JSON.stringify(response.data.graph.nodesData)
            );
            this.changedData = JSON.parse(
              JSON.stringify(response.data.graph.nodesData)
            );
            this.data = JSON.parse(
              JSON.stringify(response.data.graph.nodesData)
            );
            this.items = this.nodes();
            this.setMaxSensitivityValues();
            this.isLoading = false;
          } else {
            setTimeout(this.loadJsonFromDb, 2000);
          }
        })
        .catch(error => {
          console.log("error: " + error);
        });
    },
    restore() {
      this.changedData = JSON.parse(JSON.stringify(this.originalData));
      this.data = JSON.parse(JSON.stringify(this.originalData));
      this.items = this.nodes();
      this.setMaxSensitivityValues();
    },
    clearMergeFields() {
      this.nodeNameA = null;
      this.nodeNameB = null;
    },
    saveToFile() {
      const blob = new Blob([JSON.stringify(this.changedData)], {
        type: "application/json;charset=utf-8"
      });
      saveAs(blob, "graphData.json");
    },
    loadFromFile() {
      if (this.fileToUpload) {
        const reader = new FileReader();
        reader.addEventListener("load", event => {
          const tmpData = event.target.result.toString();
          this.changedData = JSON.parse(tmpData);
          this.originalData = JSON.parse(tmpData);
          this.data = JSON.parse(tmpData);
          this.items = this.nodes();
          this.setMaxSensitivityValues();
        });
        reader.readAsText(this.fileToUpload, "utf-8");
      } else {
        this.isFileToUpload = true;
      }
    },
    saveGraphToPng() {
      saveSvgAsPng(document.getElementById("forceGraph-svg"), "graph.png", {
        backgroundColor: "white"
      });
    },
    setMaxSensitivityValues() {
      this.data.links.forEach(item => {
        if (item.value > this.sliderMaxEdges) {
          this.sliderMaxEdges = item.value;
        }
      });
      this.data.nodes.forEach(item => {
        if (item.occurrence > this.sliderMaxNodes) {
          this.sliderMaxNodes = item.occurrence;
        }
      });
      this.sliderNodes = this.sliderMaxNodes;
      this.sliderEdges = this.sliderMaxEdges;
    }
  }
};
</script>
