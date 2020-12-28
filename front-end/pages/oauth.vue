<template>
  <div>
    <v-card class="py-8 px-6 pa-md-16">
      <v-card-title>Verifying Your account</v-card-title>
      <v-card-subtitle v-if="error.length > 0">{{ error }}</v-card-subtitle>
      <v-card-subtitle v-else-if="!loggedIn">Redirecting...</v-card-subtitle>
      <v-card-subtitle v-else>Welcome !</v-card-subtitle>
    </v-card>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  layout: 'auth',
  data() {
    return {
      error: '',
      loggedIn: false,
    }
  },
  created(): void {
    if (process.client) {
      this.googleLogin()
    }
  },
  methods: {
    googleLogin(): void {
      this.loggedIn = false
      this.error = ''
      this.$axios
        .$post('/api/auth/google/', {
          code: this.$route.query.code,
          state: this.$route.query.state,
        })
        .then(({ key }) => {
          this.loggedIn = true
          this.$auth.setUserToken(key).then(() => {
            this.$router.push('/')
          })
        })
        .catch(() => {
          this.error = 'Cannot login using Google, please try again later'
        })
    },
  },
})
</script>
