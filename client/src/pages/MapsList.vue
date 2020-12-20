<template>
  <div style="background-color: white">
    <table style="width:100%">
      <tr>
        <th style="text-align: center">Id</th>
        <th style="text-align: center">Nazwa</th>
        <th style="text-align: center">Status</th>
        <th style="text-align: center">Wyświetl</th>
      </tr>
      <tr v-for="(item, index) in literaryMaps" :key="index">
        <td class="text-center">{{ item[0] }}</td>
        <td class="text-center">{{ item[1] }}</td>
        <td class="text-center">
          <div v-if="item[2] === 1">Gotowe</div>
          <div v-else>W trakcie analizy</div>
        </td>
        <td class="text-center">
          <v-btn
            :disabled="!item[2]"
            color="primary"
            :to="{ name: 'VisualiseLocations', params: { id: item[0] } }"
            >Przejdź</v-btn
          >
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      literaryMaps: []
    };
  },
  created() {
    axios
      .get("http://127.0.0.1:5000/literaryMaps")
      .then(response => {
        this.literaryMaps = response.data.literaryMaps;
        console.log(response.data.literaryMaps);
      })
      .catch(e => {
        this.errors.push(e);
      });
  }
};
</script>

<style scoped>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td,
th {
  border: 1px solid #9dbefa;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #9dbefa;
}
</style>
