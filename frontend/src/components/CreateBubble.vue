<template>
<div>
      <NavBar :key="componentKey" />
    <loading :active.sync="loading"></loading>
  <div style="margin: 20px 20px">

    <h3>Bubble Creation</h3>

    <form class="container-fluid">
      <div class="mb-3 row">
        <!-- Bubble Name -->
        <div class="col">
          <label for="Bubble Name" class="form-label">Bubble Name</label>
          <input
            type="text"
            class="form-control"
            id="Bubble Name"
            v-model="bubble_name"
          />
        </div>
      </div>

      <div class="mb-3 row">
        <!-- Module name -->
        <div class="col">
          <label for="module" class="form-label">Module</label>
          <select v-model="selected_module" class="form-select">
            <option
              v-for="(mod_name, mod_code) in all_modules"
              :value="mod_code"
              :key="mod_code"
            >
              {{ mod_code }}: {{ mod_name }}
            </option>
          </select>
        </div>
        <!-- Max Capacity -->
        <div class="col">
          <label for="max" class="form-label">Maximum Capacity</label>
          <input
            class="form-control"
            type="number"
            d="max"
            v-model="max_capacity"
          />
        </div>

        <!-- Time -->
        <div class="col">
          <label for="meeting-time" class="form-label"
            >Choose a time for your appointment:</label
          >
          <input
            class="form-control"
            type="datetime-local"
            id="meeting-time"
            name="meeting-time"
            v-model="current_date"
            :min="current_date"
          />
        </div>
      </div>

      <!-- Agenda -->
      <div class="mb-3 row">
        <div class="col">
          <label for="agenda" class="form-label">Agenda</label>
          <textarea
            id="agenda"
            rows="6"
            class="form-control"
            v-model="agenda"
          ></textarea>
        </div>
      </div>

      <!-- submit button -->
      <div style="text-align: end">
        <button
          type="submit"
          class="btn btn-primary"
          v-on:click="submitBubble_details()"
        >
          Submit
        </button>
      </div>
    </form>
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
  name: "CreateBubble",
  data() {
    return {
      all_modules: "nihao ma",
      selected_module: "",
      current_date: "",
      agenda: "",
      max_capacity: "",
      bubble_name: "",
      // files: "",
      role: "owner",
      componentKey: 0,
      loading: false,
    };
  },

  components: {
    NavBar,
    Loading
  },
  created() {
    if (localStorage.token) {
      // decode token
      var jwt = localStorage.token;
      var tokens = jwt.split(".");
      // extract email and name
      var details = atob(tokens[1]);
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

    // Get the current date
    callDate: function () {
      var currentDate = new Date();
      var year = currentDate.getFullYear();
      var month = currentDate.getMonth();
      var date = currentDate.getDate();
      var hour = currentDate.getHours();
      var minutes = currentDate.getMinutes();

      // console.log(currentDate.getDate())

      console.log(currentDate);
      if (month + 1 < 10) {
        month = "0" + (month + 1);
      }

      if (date < 10) {
        date = "0" + date;
      }

      if (hour < 10) {
        hour = "0" + hour;
      }

      if (minutes < 10) {
        minutes = "0" + minutes;
      }

      var string = year + "-" + month + "-" + date + "T" + hour + ":" + minutes;
      console.log(string);

      this.current_date = string;
    },

    // Convert form time to unix
    toTimestamp: function (year, month, day, hour, minute) {
      // Date.prototype.addHours = function(hours) {
      //   this.setTime(this.getTime() + (hours*60*60*1000));
      //   return this;
      // }
      var datum = new Date(Date.UTC(year, month - 1, day, hour, minute));
      // datum = datum.addHours(8);
      console.log(datum.getTime() / 1000);
      return datum.getTime() / 1000;
    },

    // Bubble creation (Excluding uploading of files)
    submitBubble_details: function () {
      // check for missing values
      if (
        this.current_date == "" ||
        this.selected_module == "" ||
        this.agenda == "" ||
        this.max_capacity == "" ||
        this.bubble_name == ""
      ) {
        alert(
          "There are still empty fields! Please ensure that everything is filled up before proceeding"
        );
      } else {
         this.loading = true;
        // Post data in to serve
        var year = parseInt(this.current_date.slice(0, 4));
        var month = parseInt(this.current_date.slice(5, 7));
        var day = parseInt(this.current_date.slice(8, 10));
        var hour = parseInt(this.current_date.slice(11, 13));
        var minute = parseInt(this.current_date.slice(14, 16));

        const data = {
          bubble_name: this.bubble_name,
          meet_timestamp: parseInt(
            this.toTimestamp(year, month, day, hour, minute)
          ),
          capacity: this.max_capacity,
          agenda: this.agenda,
          module_code: this.selected_module,
        };

        console.log("SUBMITTED");
        axios
          .post(HOSTNAME + "/api/bubble/one", data, {
            headers: { Authorization: `Bearer ${localStorage.token}` },
          })
          .then((response) => {
            this.loading = true;
            console.log(response);
            alert("Bubble created successfully!!!!");
            // this.$router.push("/active");
          })
          .catch((err) => {
            this.loading = true;
            console.log(err);
            alert("Failed");
          });
     
        this.$router.push("/active");
        
      }
    },

  },

  mounted() {
    axios
      .get(HOSTNAME + "/api/bubble/module/all", {
        headers: { Authorization: `Bearer ${localStorage.token}` },
      })

      .then((response) => {
        console.log(response.data.data);
        console.log("hi");
        this.all_modules = response.data.data;
      });

    this.callDate();
  },
};
</script>

<style>
</style>