<template >
  <div>
    <NavBar :key="componentKey"/>
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

      </div>

      <!-- Show Verfied Modules -->
      <div v-for="module in verified_modules" :key="module.module_code">
        <div
          v-if="module.email == email"
          style="
            padding: 20px;
            margin-bottom: 10px;
            border-bottom: 1px solid grey;
          "
          class="row"
        >
          <div class="col">{{ module.module_code }}</div>

          <div class="col">
            <button
              type="button"
              class="btn btn-secondary"
              v-on:click="deleteMod(module.module_code)"
              :value="module.module_code"
              style="float: right"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Button to verify modules -->
      <button
        class="btn btn-secondary"
        style="float: right"
        v-on:click="verification_form"
      >
        Add New Module
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
        <h1 class="display-4">Add New Module</h1>

        <div class="mb-3 row">
          <!-- Module name -->
          <div class="col">
            <label class="form-label">Module</label> <br>
            <select v-model="selected_module" class="form-select">
              <option
                v-for="mod in all_modules"
                :value="mod.module_code"
                :key="mod.module_code"
              >
                {{ mod.module_code }}: {{ mod.module_name }}
              </option>
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
              By checking this box, I hereby declare that I am currently taking this module. Any discrepancy discovered shall result in my
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
import { HOSTNAME } from "../config.js";

export default {
  name: "VerifiedMods",
  data() {
    return {
      verified_modules: "",
      all_modules: "",
      email: "p@gmail.com",
      show_form: "",
      selected_module: "",
      verification_checkbox: "",
      componentKey:0,
    };
  },
    components:{
    NavBar,
  },
  created() {
    if (localStorage.token) {
      // decode token
      var jwt = localStorage.token;
      var tokens = jwt.split(".");
      // extract email and name
      var details = atob(tokens[1]);
      this.email = JSON.parse(details).email;
    }
    else {
      //redirect to login
      this.$router.push('/');
    }
  },
  mounted() {
    axios
      .get(HOSTNAME + "/api/module_verification/own")
      .then(
        (response) => (
          (this.verified_modules = response.data.data.module),
          console.log(response)
        )
      );

    axios
      .get(HOSTNAME + "/api/module")
      .then(
        (response) => (
          (this.all_modules = response.data.data.module),
          console.log(response.data.data.module)
        )
      );
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
        this.verification_checkbox == false
      ) {
        alert("Please ensure that all fields are filled");
      } else {
        // axios
        //   .post("http://localhost:8000/user/signup", {
        //     email: "c@gmail.com",
        //     name: "c",
        //     password: "c",
        //   })
        //   .then((response) => {
        //     console.log(response);
        //   });
      }
    },

    deleteMod: function (module_code) {
      // this.mod_deleted="<hr><b>hello</b>";

      alert("You are deleting " + module_code + " from your profile");
      console.log(module_code);
    },
  },
};
</script>