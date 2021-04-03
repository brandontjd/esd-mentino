<template>
  <div>
    <TopBar :key="componentKey" />
     <loading :active.sync="loading"></loading>
    <div class="container-fluid" style="margin-top: 25px">
      <div class="row justify-content-center">
        <div class="col-sm-6 jumbotron" id="header" style="background: #242291">
          <h1 class="display-5" style="color: white">
            Welcome to The Mentoring Bubble!
          </h1>
          <p class="lead" style="color: white">
            Log in to access your account!
          </p>
          <p class="pt-3" style="color: white; font-size: small">
            Don't have an account? Click
            <a
              @click="$router.push({ name: 'Signup' })"
              style="text-decoration: underline; color: sandybrown"
              >here</a
            >
            to sign up!
          </p>
        </div>
      </div>
      <div class="row justify-content-center" id="logIn">
        <div class="col-sm-6">
          <div class="form-group">
            <label>Email</label>
            <input
              type="email"
              class="form-control"
              v-model="email"
              placeholder="Email"
            />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input
              type="password"
              class="form-control"
              v-model="password"
              placeholder="Password"
            />
          </div>
          <div class="text-center">
            <button class="btn btn-primary btn-block" @click.prevent="handleSubmit()">
              Login
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
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
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
      componentKey: 0,
      loading: false,
    };
  },
  components: {
    TopBar,
    Loading
  },
  methods: {
    // to refresh the navbar
    forceRerender() {
      this.componentKey += 1;
    },

    handleSubmit() {
      this.loading = true;

      axios
        .post(HOSTNAME + "/api/user/login", {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          var result = response.data;
          localStorage.setItem("token", result.data);
          this.$router.push("/explore");
        })
        .catch((err) => {
          console.err(err);
          alert("Email/password incorrect!");
        }).finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>
