<template>
  <v-card class="pa-12">
    <v-form ref="form" v-model="valid" @submit.prevent="submitForm">
      <v-text-field
        v-model="password"
        type="password"
        :rules="[required]"
        :error-messages="errors"
        label="New Password"
      ></v-text-field>
      <v-text-field
        v-model="passwordConfirmation"
        type="password"
        :rules="[required, passwordIdentical]"
        label="Confirmation"
      ></v-text-field>
      <v-btn :disabled="!valid" :loading="loading" type="submit" class="mt-6">
        RESET PASSWORD
      </v-btn>
    </v-form>
  </v-card>
</template>

<script>
import { required } from '../../../mixins/validator'
export default {
  layout: 'auth',
  data() {
    return {
      password: null,
      passwordConfirmation: null,
      required,
      errors: null,
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
      this.errors = null
      this.$refs.form.validate()
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
        .catch((e) => {
          if (e.response && e.response.data && e.response.data.new_password) {
            this.errors = e.response.data.new_password
          } else {
            this.errors = 'Server error, please try again later'
          }
          this.loading = false
        })
    },
  },
}
</script>
