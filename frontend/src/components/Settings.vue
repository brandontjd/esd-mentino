<template >
  <div>
    <NavBar :key="componentKey" />
    <loading :active.sync="loading"></loading>
    <div style="margin: 50px 15%">
      <div>
        <!-- Need to retrieve details from API -->
        <h2 style="border-bottom: 1px solid grey">{{ name }}</h2>
        <button style="float: right" class="btn btn-secondary" @click="clickEditPassword">
          Edit Password
        </button>
        <div>Email: {{ email }}</div>
      </div>

      <!-- Currently Verified Modules -->
      <h4 style="margin-top: 60px; border-bottom: 1px solid grey">
        Modules Verified
      </h4>
      <button
        style="float: right"
        class="btn btn-secondary"
        @click="$router.push({ name: 'VerifiedMods' })"
      >
        Add Module
      </button>
      <div v-for="(grade, module) in verified_modules" :key="module">
        <li>{{ module }} : {{ grade }}</li>
      </div>

    </div>
  </div>
</template>


<script>
import axios from "axios";
import NavBar from "./NavBar";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";
import { HOSTNAME } from "../config.js";

export default {
  name: "Settings",
  data() {
    return {
      verified_modules: "",
      email: "",
      name: "",
      componentKey: 0,
      loading: false,
    };
  },
  components: {
    NavBar,
    Loading,
  },

  async mounted() {
    this.loading = true;

    setTimeout(() => {
      this.isLoading = false;
    }, 5000);

    const verified_mods = await axios.get(
      HOSTNAME + "/api/bubble/module_verification/own",
      {
        headers: { Authorization: `Bearer ${localStorage.token}` },
      }
    );
    this.verified_modules = verified_mods.data.data;

    this.loading = false;
  },

  created() {
    if (localStorage.token) {
      // decode token
      var jwt = localStorage.token;
      var tokens = jwt.split(".");
      // extract email and name
      var details = atob(tokens[1]);
      this.name = JSON.parse(details).name;
      this.email = JSON.parse(details).email;
    } else {
      //redirect to login
      this.$router.push("/");
    }
  },

  methods: {
    // to refresh the navbar
    forceRerender() {
      this.componentKey += 1;
    },
    clickEditPassword() {
      alert("Not implemented for this project ☹️");
    }
  },
};
</script>