<template>
  <v-layout>
    <v-flex class="text-center">
      <v-input v-model="login"></v-input>
      <v-input v-model="password"></v-input>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      login: null,
      password: null,
    }
  },
  methods: {
    loggin() {},
  },
}
</script>
