<template>
  <v-card class="pa-12">
    <v-form ref="form" v-model="valid" @submit.prevent="submitForm">
      <v-text-field
        id="password"
        v-model="password"
        type="password"
        :rules="[required, ...weakPasswordRules]"
        :error-messages="apiErrors"
        label="New Password"
      />
      <v-text-field
        id="password-confirmation"
        v-model="passwordConfirmation"
        type="password"
        :rules="[required, passwordIdentical]"
        label="Confirmation"
      />
      <v-btn
        id="submit"
        :disabled="!valid"
        :loading="loading"
        type="submit"
        class="mt-6"
      >
        RESET PASSWORD
      </v-btn>
    </v-form>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { required, weakPasswordRules } from '../../../mixins/validator'
export default Vue.extend({
  layout: 'auth',
  data() {
    return {
      password: '',
      passwordConfirmation: '',
      required,
      weakPasswordRules,
      apiErrors: '',
      loading: false,
      valid: false,
    }
  },
  watch: {
    password() {
      this.validate()
    },
    passwordConfirmation() {
      this.validate()
    },
  },
  methods: {
    passwordIdentical() {
      return (
        this.password === this.passwordConfirmation ||
        'Passwords are not matching'
      )
    },
    validate() {
      this.apiErrors = ''
      const form: any = this.$refs.form
      form.validate()
    },
    submitForm() {
      this.loading = true
      this.$axios
        .$post('api/auth/users/reset_password_confirm/', {
          uid: this.$route.params.uid,
          token: this.$route.params.token,
          new_password: this.password,
        })
        .then(() => {
          this.$router.push('/login')
        })
        .catch(() => {
          this.loading = false
          this.apiErrors = 'Sorry, cannot verify your identity'
        })
    },
  },
})
</script>
