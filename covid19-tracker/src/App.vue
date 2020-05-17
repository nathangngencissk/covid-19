<template>
  <v-app>
    <v-app-bar app color="red darken-3" dark>
      <div class="d-flex align-center">
        <v-toolbar-title>Covid-19 Tracker</v-toolbar-title>
      </div>

      <v-spacer></v-spacer>

      <v-btn href="https://d3gdzw78a0j76y.cloudfront.net/latest_report.csv" download text>
        <span class="mr-2">Download CSV</span>
        <v-icon>fas fa-download</v-icon>
      </v-btn>
      <v-btn href="https://github.com/nathangngencissk/covid-19" target="_blank" text>
        <span class="mr-2">Github Repo</span>
        <v-icon>fab fa-github</v-icon>
      </v-btn>
    </v-app-bar>

    <v-content>
      <v-data-table
        :headers="headers"
        :items="items"
        :items-per-page="15"
        :loading="loading"
        class="elevation-1"
      ></v-data-table>
    </v-content>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  name: "App",

  components: {},

  data() {
    return {
      loading: true,
      headers: [
        { text: "Country/Region", value: "country_region" },
        { text: "Province/State", value: "province_state" },
        { text: "County (US only)", value: "county_US" },
        { text: "Confirmed", value: "confirmed" },
        { text: "Active", value: "active" },
        { text: "Recovered", value: "recovered" },
        { text: "Deaths", value: "deaths" }
      ],
      items: []
    };
  },

  mounted() {
    axios
      .get(
        "https://7zd2em8b4g.execute-api.us-east-1.amazonaws.com/Prod/covid19"
      )
      .then(response => {
        this.items = response.data.items;
        this.loading = false;
      });
  }
};
</script>
