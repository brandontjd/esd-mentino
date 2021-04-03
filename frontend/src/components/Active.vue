<template>
  <div>
    <!-- links -->
    <!-- Displaying of cards -->
    <NavBar :key="componentKey" />
    <loading :active.sync="loading"></loading>

    <h3 v-if="all_bubbles_selected.length == 0" style="text-align: center">
      <br /><br />
      No active bubbles :(
    </h3>

    <div v-else>
      <h4 style="padding: 20px 0px 10px 40px">All Active Bubbles</h4>
      <div
        v-for="selected_bubble in all_bubbles_selected"
        style="display: inline-block; margin: 5px 5px"
        :key="selected_bubble.bubble_id"
      >

      
        <div class="card" style="width: 19rem;" >
          <div class="card-body">
            <h5 class="card-title">
              {{ selected_bubble.bubble_name }}
              <span
                v-if="selected_bubble.role != 'None'"
                class="badge badge-warning"
              >
                {{ selected_bubble.role }}
              </span>
            </h5>
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
                Pending Confirmation
            </span>




          </div>
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
import NavBar from "./NavBar";
// Import component
import Loading from "vue-loading-overlay";
// Import stylesheet
import "vue-loading-overlay/dist/vue-loading.css";


export default {
  name: "Active",

  data() {
    return {
      // all_bubbles: "nihao ma",
      // selected: "",
      all_bubbles_selected: "hello",
      moreDetails_bubble_id: "",
      email: "",
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

    const all_bubbles_selected = await axios.get( "http://localhost:8000/api/bubble/all",
      {
        headers: {
          Authorization: `Bearer ${localStorage.token}`,
        },
      }
    );
    console.log(all_bubbles_selected.data);
    this.all_bubbles_selected = all_bubbles_selected.data.data.active_bubbles;

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