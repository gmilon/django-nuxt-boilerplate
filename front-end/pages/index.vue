<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <v-card class="pa-10 mt-16">
        <div class="text-center">
          <logo />
        </div>
        <v-card-title class="headline">
          Welcome to the landing page
        </v-card-title>
        <v-card-text>
          <p>This page is public and available for everyone</p>
          <p>
            For more information on this project, check out the
            <a
              href="https://github.com/gmilon/django-nuxt-boilerplate"
              target="_blank"
              rel="noopener noreferrer"
            >
              documentation
            </a>
          </p>
          <hr class="my-3" />
          <a
            href="https://nuxtjs.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Nuxt Documentation
          </a>
          <br />
          <a
            href="https://github.com/nuxt/nuxt.js"
            target="_blank"
            rel="noopener noreferrer"
          >
            Nuxt GitHub
          </a>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn v-if="!$auth.loggedIn" color="primary" nuxt to="/login">
            Login
          </v-btn>
          <v-btn v-else nuxt to="/todos" color="primary">
            Check my todos
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from 'vue'
import Logo from '@/components/Logo.vue'

export default Vue.extend({
  layout: 'public',
  components: {
    Logo,
  },
})
</script>
