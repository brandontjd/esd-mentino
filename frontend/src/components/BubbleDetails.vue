<template>
  <div>
    <NavBar :key="componentKey" />
    <loading :active.sync="loading"></loading>
    <div id="app" style="margin: 50px 15%">
      <div class="container">
        <div class="row">
          <h3 class="col">
            {{ bubble_details.bubble_name }}
            <span
              v-if="bubble_details.role != 'None'"
              class="badge badge-warning capitalizeLetter"
            >
              {{ bubble_details.role }}
            </span>
          </h3>
        </div>

        <!-- modulecode -->
        <div class="row">
          <div class="col">
            <h6>Module Name:</h6>
            <div>{{ bubble_details.module_code }}</div>
          </div>

          <!-- capacity -->
          <div class="col">
            <h6>Maximum Capacity:</h6>
            <div>{{ bubble_details.capacity }}</div>
          </div>

          <!-- time -->
          <div class="col">
            <h6>Time of workshop:</h6>
            <div>
              {{ timeConverter(bubble_details.meet_timestamp) }}
            </div>
          </div>
        </div>

        <br /><br />
        <!-- agenda -->
        <div class="row">
          <!-- mentor found -->
          <div class="col">
            <h6>Mentor Found?</h6>
            <div v-if="bubble_details.mentor_found">Yes</div>
            <div v-else>No</div>
          </div>

          <!-- number of Particpants -->
          <div class="col">
            <h6>Current Number of Participants</h6>
            <div>{{ bubble_details.num_participants }}</div>
          </div>
          <div class="col"></div>
        </div>

        <br /><br />

        <!-- agenda -->
        <div class="row">
          <div class="col">
            <h6>Agenda</h6>
            <div>{{ bubble_details.agenda }}</div>
          </div>
        </div>

        <br /><br />

        <!-- Show list of files Attachments -->

        <div class="row">
          <div class="col">
            <h6>File Attachments</h6>
            <div v-if="bubble_details.files && bubble_details.files.length > 0">
              <div v-for="file in bubble_details.files" :key="file.blob_url">
                <li v-if="file.description">
                  {{ file.description }}:
                  <a :href="file.blob_url">{{ file.blob_url }}</a>
                </li>
              </div>
            </div>
            <div v-else>
              <li>No Attachments Available</li>
            </div>
          </div>
        </div>

        <br />
        <!-- if user has already joined, as mentor, "Add File" will show -->
        <button
          type="button"
          class="btn btn-light"
          style="padding: 10px"
          v-on:click="showform"
          v-if="bubble_details.role === 'mentor'"
        >
          Add File
        </button>

        <br /><br />
        <!-- buttons -->
        <button
          v-if="bubble_details.role === 'None'"
          class="btn btn-secondary ml-3"
          style="float: right"
          @click.prevent="joinAsMentee"
        >
          Join Bubble as Mentee
        </button>
        <button
          v-if="bubble_details.role === 'None' && !bubble_details.mentor_found"
          class="btn btn-secondary"
          style="float: right"
          @click.prevent="joinAsMentor"
        >
          Join Bubble as Mentor
        </button>
      </div>
    </div>

    <!-- Add new file form  -->
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
        <h1 class="display-4">Add New Files</h1>

        <div class="mb-3 row">
          <div class="col">
            <label for="description" class="form-label"
              >Description of file</label
            >
            <input
              type="text"
              id="description"
              class="form-control"
              v-model="description"
            />
          </div>

          <!-- File upload -->
          <div class="col">
            <label for="files" class="form-label"
              >Select a file: (Max size: 10MB; Allowed extensions: pdf, docx,
              pptx, txt)</label
            >
            <input
              type="file"
              id="files"
              name="file"
              ref="file"
              class="form-control"
              v-on:change="handleFileUpload()"
            />
          </div>
        </div>
        <!-- Add new module button -->
        <button
          type="button"
          class="btn btn-primary"
          style="float: right"
          v-on:click="submitFile"
        >
          Add
        </button>
      </div>
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
  name: "BubbleDetails",
  data() {
    return {
      bubble_id: "",
      bubble_details: "",
      verified_modules: "",
      show_form: "",
      description: "",
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
    if (localStorage.moreDetails_bubble_id) {
      this.bubble_id = localStorage.moreDetails_bubble_id;
    }
    const bubble_details = await axios.get(
      HOSTNAME + "/api/bubble/one/" + this.bubble_id,
      {
        headers: { Authorization: `Bearer ${localStorage.token}` },
      }
    );
    this.bubble_details = bubble_details.data.data;
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
  methods: {
    // to refresh the navbar
    forceRerender() {
      this.componentKey += 1;
    },
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
      // var sec = "0" + a.getSeconds();
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
      // + ":" + sec.substr(-2);
      return time;
    },

    showform() {
      if (this.show_form == "") {
        this.show_form = "Show";
      } else {
        this.show_form = "";
      }
    },

    // Upload new file button
    submitFile() {
      this.loading = true;
      let formData = new FormData();
      formData.append("file", this.file);
      formData.append("bubble_id", this.bubble_details.bubble_id);
      formData.append("description", this.description);

      axios
        .post(HOSTNAME + "/api/bubble/upload", formData, {
          headers: {
            Authorization: `Bearer ${localStorage.token}`,

            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          if (response.data.code == 415) {
            alert(
              "Invalid file type! Only 'pdf', 'docx', 'pptx', 'txt' allowed!"
            );
          } else if (response.data.code == 413) {
            alert("Your file size is too big!! Maximum file size is 10Mb ");
          } else {
            alert(
              "File is uploading...may take a while! Please come back later"
            );
            window.location.reload();
          }
          // this.$router.push("/active");
        })
        .catch((err) => {
          console.error(err);
          alert("Failed upload");
        })
        .finally(() => {
          this.loading = false;
        });
    },

    // Handle file changes(Part of file upload)
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },

    joinAsMentee() {
      this.loading = true;

      axios
        .post(
          HOSTNAME + "/api/bubble/join",
          {
            bubble_id: this.bubble_id,
            role: "participant",
          },
          {
            headers: { Authorization: `Bearer ${localStorage.token}` },
          }
        )
        .then((response) => {
          alert(response.data.message);
          this.$router.push("/active");
        })
        .catch((err) => {
          console.error(err);
          alert("Failed to join as Mentee!");
        }).finally(() => {
          this.loading = false;
        });
    },

    joinAsMentor() {
      this.loading = true;
      setTimeout(() => {
        this.isLoading = false;
      }, 5000);

      axios
        .post(
          HOSTNAME + "/api/bubble/join",
          {
            bubble_id: this.bubble_id,
            role: "mentor",
          },
          {
            headers: { Authorization: `Bearer ${localStorage.token}` },
          }
        )
        .then((response) => {
          if (response.data.code == 403) {
            alert(
              "Failed to join as Mentor! Please verify module under Settings first!"
            );
          } else if (response.data.code == 201) {
            alert(response.data.message);
            this.$router.push("/active");
          }
        })
        .catch((err) => {
          console.error(err);
          alert("Failed to join as Mentor!");
        }).finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style scoped>
  .capitalizeLetter {
    text-transform: capitalize;
  }
</style>  