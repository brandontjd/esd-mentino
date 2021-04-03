<template>
  <div>
    <NavBar :key="componentKey" />
    <loading :active.sync="loading"></loading>
    <!-- links -->
    <!-- Filters -->
    <div
      class="jumbotron"
      style="background-position: center; height: 200px"
      :style="{
        'background-image':
          'url(' + require('../assets/explore_header.png') + ')',
      }"
    >
      <br /><br />
      <div
        class="container"
        style="
          background-color: rgb(182, 182, 182);
          padding: 40px;
          border-radius: 10px;
        "
      >
        <div style="text-align: center">
          <h3 style="display: inline-block">Module Code:</h3>
          <select
            v-model="selected"
            class="form-select"
            style="width: 400px; display: inline-table"
          >
            <option disabled>Please select one</option>
            <option value="all">All</option>
            <option
              v-for="module in this.all_modules"
              :value="module"
              :key="module"
            >
              {{ module }}
            </option>
          </select>
          <!-- <span>Selected: {{ selected }}</span> -->
          <button v-on:click="filterCards" class="btn btn-secondary">
            Filter
          </button>
        </div>
      </div>
    </div>

    <br /><br /><br />

    <!-- Displaying of cards -->
    <div
      v-for="selected_bubble in all_bubbles_selected"
      style="display: inline-block; margin: 5px 10px"
      :key="selected_bubble.bubble_id"
    >
      <div class="card" style="width: 18rem">
        <div class="card-body">
          <h5 class="card-title">{{ selected_bubble.bubble_name }}</h5>
          <h6 class="card-subtitle mb-2 text-muted">
            Module Code: {{ selected_bubble.module_code }}
          </h6>
          <h6 class="card-subtitle mb-2 text-muted">
            Date & Time: {{ timeConverter(selected_bubble.meet_timestamp) }}
          </h6>
          <!-- <p class="card-text">{{ selected_bubble.agenda }}</p> -->
          <button
            style="margin-top: 10px"
            type="button"
            class="btn btn-outline-warning"
            :value="selected_bubble.bubble_id"
            v-on:click="moreDetails(selected_bubble.bubble_id)"
          >
            details
          </button>

           <span style="color: green;  font-weight:bold; float: right; padding: 15px 0px" 
            v-if="selected_bubble.mentor_found">Workshop Confirmed</span>

            <span v-else style="color: red;  font-weight:bold; float: right; padding: 15px 0px">
              Awaiting Mentor
            </span>

        </div>
      </div>
    </div>

    <!-- Create Bubble -->
    <button
      type="button"
      class="btn btn-secondary btn-lg"
      style="position: fixed; bottom: 30pt; right: 30pt"
      @click="$router.push({ name: 'CreateBubble' })"
    >
      Create Bubble
    </button>

  </div>
</template>

<script >
import axios from "axios";
import NavBar from "./NavBar"
// Import component
import Loading from "vue-loading-overlay";
// Import stylesheet
import "vue-loading-overlay/dist/vue-loading.css";
import { HOSTNAME } from "../config.js";

export default {
  name: "Explore",

  data() {
    return {
      all_bubbles: "nihao ma",
      selected: "",
      all_bubbles_selected: "hello",
      moreDetails_bubble_id: "",
      email: "",
      all_modules:[], 
      componentKey:0,
      loading:false,
    };
  },

  components:{
    NavBar,
    Loading
  },
  
  async mounted(){

    this.loading = true;

    setTimeout(() => {
      this.isLoading = false;
    }, 5000);

    const all_bubbles= await axios.get(
      HOSTNAME + "/api/bubble/all", {
        headers: { Authorization: `Bearer ${localStorage.token}` },
      });

        console.log(all_bubbles.data);
        this.all_bubbles = all_bubbles.data.data.other_bubbles;
        this.all_bubbles_selected = this.all_bubbles;

        // To get all unique modules
        for(let bubble of this.all_bubbles){
          console.log(bubble.module_code);
          if(this.all_modules.includes(bubble.module_code) == false ){
            this.all_modules.push(bubble.module_code);
          }
        }
        console.log(this.all_modules);

        this.loading = false;
    
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
  // Details about the task are passed from parent
  props: [],
  methods: {

    // to refresh the navbar
    forceRerender() {
      this.componentKey += 1;  
    },

    filterCards: function () {
      this.all_bubbles_selected = [];
      console.log("selected", this.selected);

      if (this.selected == "all") {
        this.all_bubbles_selected = this.all_bubbles;
      } else {
        for (let bubble in this.all_bubbles) {
          if (this.all_bubbles[bubble].module_code == this.selected) {
            this.all_bubbles_selected.push(this.all_bubbles[bubble]);
          }
        }
      }
    },

    // Convert unix timestamp to date time format
    timeConverter: function (UNIX_timestamp) {
      var a = new Date(UNIX_timestamp * 1000);
      Date.prototype.removeHours = function (hours) {
        this.setTime(this.getTime() - hours * 60 * 60 * 1000);
        return this;
      };
      a = a.removeHours(8);
      var months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ];
      var year = a.getFullYear();
      var month = months[a.getMonth()];
      var date = a.getDate();
      var hour = "0" + a.getHours();
      var min = "0" + a.getMinutes();
      // var sec = a.getSeconds();
      var time =
        date +
        " " +
        month +
        " " +
        year +
        " " +
        hour.substr(-2) +
        ":" +
        min.substr(-2);
      return time;
    },


    moreDetails: function (bubble_id) {
      // console.log(bubble_id);
      this.moreDetails_bubble_id = bubble_id;
      console.log(this.moreDetails_bubble_id);
      localStorage.moreDetails_bubble_id = this.moreDetails_bubble_id;
      this.$router.push({ name: "BubbleDetails" });
    },
    



  },
};
</script>

<style>
</style>