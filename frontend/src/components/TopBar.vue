<template>
  <nav
    class="navbar navbar-expand-lg"
    style="background-color: rgb(28, 28, 76); color: white; font-size: 25px; padding-top: 20px"
  >
    <!-- <div class="container-fluid"> -->
    <div class="navbar-brand">The Mentoring Bubble</div>

    <!-- <div style="padding-top: 20px">
      <ul >
      <li class="nav-item active">
        <router-link to="/explore">Explore</router-link>
      </li>
      <li class="nav-item active">
        <router-link to="/active">Active</router-link>
      </li>
      <li class="nav-item active">
        <router-link to="/settings">Settings</router-link>
      </li>
      <li class="nav-item">
        <button v-if=" showLogout " type="button" class="btn btn-primary" @click="logOut()">
          Logout
        </button>
        <div v-else></div>
      </li>
    </ul>
    </div> -->

    <!-- </div> -->
  </nav>
</template>

<script>
export default {
  name: "TopBar",
  data() {
    return {
      jwt: localStorage.token,
      showLogout: ''
    }  
  },
  created() {
    // setInterval(() => {
      if (localStorage.token) {
        this.showLogout = true;
      }
      else {
        this.showLogout = false;
      }
    // }, 1)
  },
  methods: {
    logOut() {
      if (localStorage.token) {
        localStorage.removeItem("token");
        this.showLogout= false;
      }
      this.$router.push("/");
    },

    checkJWT: function() {
      setInterval( function() {
          if (!localStorage.token) {
            return false;
          }
          else {
            return true;
          }
        }, 1
      );
    }

  },
  watch: {
    jwt() {
      console.log(this.jwt);
      console.log(this.showLogout);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
