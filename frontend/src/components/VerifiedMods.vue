<template >
  <div >
    <NavBar :key="componentKey" />

    <loading :active.sync="loading"></loading>

    <div style="margin: 50px 15%">
      <h2 style="margin-top: 60px; bottom: 0">Modules Verified</h2>

      <div
        class="row"
        style="
          padding: 20px;
          background-color: rgb(232, 232, 232);
          margin-bottom: 10px;
          border-radius: 5px;
          font-weight: Bold;
          font-size: 20px;
        "

      >
        <div class="col">Module Code</div>
        <div class="col" style="text-align: right">Grade Attained</div>
        <div class="col"></div>
      </div>

      <!-- Show Verified Modules -->
      <div
        v-for="(grade, module) in verified_modules"
        :key="module"
        id="addModsHere"
      >
        <div
          style="
            padding: 20px;
            margin-bottom: 10px;
            border-bottom: 1px solid grey;
          "
          class="row"
        >
          <div class="col">{{ module }}</div>
          <div class="col">
            {{ grade }}
          </div>
        </div>
      </div>

      <!-- Button to verify modules -->
      <button
        class="btn btn-secondary"
        style="float: right"
        v-on:click="verification_form"
      >
        Verify New Module
      </button>
    </div>

    <!-- Verify New Module's Form  -->
    <div
      class="container-fluid"
      style="
        bottom: 0;
        margin-top: 100px;
        background-color: rgb(232, 232, 232);
        padding: 60px;
      "
      v-if="show_form == 'Show'"
    >
      <div class="container">
        <h1 class="display-4">Verify New Module</h1>

        <div class="mb-3 row">
          <!-- Module name -->
          <div class="col">
            <label class="form-label">Module</label>
            <select v-model="selected_module" class="form-select">
              <option
                v-for="(title, code) in all_modules"
                :value="code"
                :key="code"
              >
                {{ code }}: {{ title }}
              </option>
            </select>
          </div>

          <div class="col">
            <!-- Grade fill -->
            <label class="form-label">Module Grade</label> <br />
            <select
              class="form-select"
              style="width: 150px"
              v-model="selected_module_grade"
            >
              <option value="A+">A+</option>
              <option value="A">A</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
            </select>
          </div>
        </div>

        <!-- Checkbox -->
        <div class="mb-3 row">
          <div class="form-check col">
            <input
              class="form-check-input"
              type="checkbox"
              value=""
              id="flexCheckDefault"
              v-model="verification_checkbox"
            />
            <label class="form-check-label" for="flexCheckDefault">
              By checking this box, I hereby declare that the grades I have
              indicated are true. Any discrepancy discovered shall result in my
              account being banned immediately.
            </label>
          </div>
        </div>

        <!-- Add new module button -->
        <button
          type="button"
          class="btn btn-primary"
          style="float: right"
          v-on:click="add_new_mod"
        >
          Verify
        </button>
      </div>

      <!-- {{ selected_module }}
      {{ selected_module_grade }}
      {{ verification_checkbox }} -->
    </div>
  </div>
</template>

<script>
import axios from "axios";
import NavBar from "./NavBar";
// Import component
import Loading from "vue-loading-overlay";
// Import stylesheet
import "vue-loading-overlay/dist/vue-loading.css";
import { HOSTNAME } from "../config.js";

export default {
  name: "VerifiedMods",
  data() {
    return {
      verified_modules: "",
      all_modules: "",
      name: "",
      email: "",
      show_form: "",
      selected_module: "",
      selected_module_grade: "",
      verification_checkbox: "",
      componentKey: 0,
      loading: false,
    };
  },
  components: {
    NavBar,
    Loading,
  },

  created() {
    if (localStorage.token) {
      // decode token
      var jwt = localStorage.token;
      var tokens = jwt.split(".");
      // extract email and name
      var details = atob(tokens[1]);
      // console.log(details);
      this.name = JSON.parse(details).name;
      this.email = JSON.parse(details).email;
    } else {
      //redirect to login
      this.$router.push("/");
    }
  },
  async mounted() {
    this.loading = true;


    const verified_mods = await axios.get(
      HOSTNAME + "/api/bubble/module_verification/own",
      {
        headers: { Authorization: `Bearer ${localStorage.token}` },
      }
    );

    this.verified_modules = verified_mods.data.data;

    const all_mods = await axios.get(
      HOSTNAME + "/api/bubble/module/all",
      {
        headers: { Authorization: `Bearer ${localStorage.token}` },
      }
    );

    this.all_modules = all_mods.data.data;
    this.loading = false;
  },

  methods: {
  
    // to refresh the navbar
    forceRerender() {
      this.componentKey += 1;
    },

    verification_form: function () {
      if (this.show_form == "") {
        this.show_form = "Show";
      } else {
        this.show_form = "";
      }
    },

    // Need to change the API
    add_new_mod: function () {
      if (
        this.selected_module == "" ||
        this.selected_module_grade == "" ||
        this.verification_checkbox == false
      ) {
        alert("Please ensure that all fields are filled");
      } else {
        axios
          .put(
            HOSTNAME + "/api/bubble/module_verification/own",
            {
              modules: [
                {
                  module_code: this.selected_module,
                  module_grade: this.selected_module_grade,
                },
              ],
            },
            { headers: { Authorization: `Bearer ${localStorage.token}` } }
          )
          .then((response) => {
            console.log(response.data.message);
            document.getElementById("addModsHere").innerHTML += `<div
                                                                      style="
                                                                        padding: 20px;
                                                                        margin-bottom: 10px;
                                                                        border-bottom: 1px solid grey;
                                                                      "
                                                                      class="row"
                                                                    >
                                                                      <div class="col">${this.selected_module}</div>
                                                                      <div class="col" >
                                                                        ${this.selected_module_grade}
                                                                      </div>
                                                                    </div>`;
            
          });

        alert("Module verified successfully!");
        window.location.reload();
      }
    },
  },
};
</script>