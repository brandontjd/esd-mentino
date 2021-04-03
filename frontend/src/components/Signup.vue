<template>
  <!-- <form> -->
  <div>
    <TopBar :key="componentKey"/>
     <loading :active.sync="loading"></loading>
    <div class="container-fluid" style="margin-top: 25px">
      <div class="row justify-content-center">
        <div class="col-sm-6 jumbotron" id="header" style="background: #242291">
          <h1 class="display-5" style="color: white">
            Join The Mentoring Bubble Today!
          </h1>
          <p class="lead" style="color: white">
            Sign up to mentor and be mentored!
          </p>
          <p class="pt-3" style="color: white; font-size: small">
            Already a user? Click
            <a
              @click="$router.push({ name: 'Login' })"
              style="text-decoration: underline; color: sandybrown"
              >here</a
            >
            to log in!
          </p>
        </div>
      </div>
      <div class="row justify-content-center" id="signUp">
        <div class="col-sm-6">
          <div class="form-group">
            <label>Name:</label>
            <input
              type="text"
              v-model="Name"
              class="form-control"
              name="Name"
              id="Name"
              placeholder="Enter your Name"
            />
          </div>
          <div class="form-group">
            <label>Email:</label>
            <input
              type="email"
              v-model="email"
              class="form-control"
              name="email"
              id="email"
              placeholder="Enter your email"
            />
          </div>
          <div class="form-group">
            <label>Password:</label>
            <input
              type="password"
              v-model="password1"
              class="form-control"
              name="password"
              id="password"
              placeholder="Enter your password"
            />
          </div>
          <div class="form-group">
            <label>Confirm Password:</label>
            <input
              type="password"
              v-model="password2"
              class="form-control"
              name="confirmedPassword"
              id="confirmedPassword"
              placeholder="Confirm your password"
            />
          </div>

          <div v-if="checkpassword()"></div>
          <div v-else class="alert alert-danger" role="alert">
            Passwords do not match!
          </div>
          <div class="text-center">
            <button
              v-if="checkAll()"
              class="btn btn-primary"
              id="submitButton"
              @click.prevent="signUp()"
            >
              Submit
            </button>
            <button v-else type="submit" class="btn btn-primary" disabled>
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- </form> -->
</template>

<script>
import axios from "axios";
import TopBar from "./TopBar"
// Import component
import Loading from "vue-loading-overlay";
// Import stylesheet
import "vue-loading-overlay/dist/vue-loading.css";
import { HOSTNAME } from "../config.js";

export default {
  name: "Signup",
  data() {
    return {
      Name: "",
      email: "",
      password1: "",
      password2: "",
      componentKey:0,
      loading:false,
    };
  },

  
  components:{
    TopBar,
    Loading
  },

  methods: {
       // to refresh the navbar
    forceRerender() {
      this.componentKey += 1;  
    },

    checkAll: function () {
      if (this.Name == "" || this.email == "") {
        return false;
      }
      if (this.password1 == "" && this.password2 == "") {
        return false;
      }
      if (this.password1 != this.password2) {
        return false;
      } else {
        if (this.password1 == this.password2) {
          return true;
        }
      }
    },
    checkpassword: function () {
      if (this.password1 != this.password2) {
        return false;
      } else {
        if (this.password1 == this.password2) {
          return true;
        }
      }
    },
    signUp() {
      this.loading = true;
      const data = {
        email: this.email,
        name: this.Name,
        password: this.password1,
      };
      axios
        .post(HOSTNAME + "/api/user/signup", data)
        .then(() => {
          alert("Account created successfully!");
          this.$router.push("/");
        })
        .catch((err) => {
          console.error(err);
          this.email = "";
          this.Name = "";
          this.password1 = "";
          this.password2 = "";
          alert("Account already exists!");
        }).finally(() =>{
          this.loading = false;
        });
      
    },
  },
};
</script>

