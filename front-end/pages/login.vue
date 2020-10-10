<template>
  <div>
    <v-card class="py-8 px-6 pa-md-16">
      <v-form ref="form" v-model="valid" @submit.prevent="submitForm">
        <v-row class="flex-column-reverse flex-md-row">
          <v-col cols="12" md="6">
            <v-text-field
              v-if="mode !== modes.forgotConfirm"
              v-model="email"
              :rules="loginRules"
              :error-messages="emailApiErrors"
              label="Email"
              required
              single-line
            ></v-text-field>
            <v-expand-transition>
              <v-text-field
                v-if="![modes.forgot, modes.forgotConfirm].includes(mode)"
                v-model="password"
                :append-icon="showPwd ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPwd ? 'text' : 'password'"
                label="Password"
                :rules="passwordRules"
                :error-messages="apiErrors.password"
                required
                single-line
                @click:append="showPwd = !showPwd"
              ></v-text-field>
            </v-expand-transition>
            <v-expand-transition>
              <v-text-field
                v-if="mode === modes.signUp"
                v-model="passwordConfirm"
                type="password"
                :rules="passwordRules"
                label="Password Confirmation"
                single-line
              ></v-text-field>
            </v-expand-transition>

            <p v-if="mode === modes.forgotConfirm">
              A reset E-mail has been sent to {{ email }}
            </p>

            <div v-if="mode !== modes.forgotConfirm" class="d-flex pt-3 mb-5">
              <v-btn
                type="submit"
                large
                block
                color="primary"
                :disabled="!valid"
                :loading="loading"
              >
                {{ submitText }}
              </v-btn>
            </div>
            <v-expand-transition>
              <div v-if="!loading">
                <p v-if="mode === modes.signIn">
                  Have not an accout yet?
                  <a href="#" @click="switchMode(modes.signUp)">Sign Up</a>
                </p>
                <p v-else>
                  Go back to
                  <a href="#" @click="switchMode(modes.signIn)">Login</a>
                </p>
                <a
                  v-if="mode !== modes.forgot"
                  href="#"
                  @click="switchMode(modes.forgot)"
                >
                  Forgot your password ?
                </a>
              </div>
            </v-expand-transition>
          </v-col>
          <v-col cols="12" md="6" class="d-flex align-center justify-center">
            <logo class="mb-10" />
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </div>
</template>

<script>
import { required, email } from '../mixins/validator'
export default {
  layout: 'auth',
  data() {
    return {
      email: null,
      password: null,
      passwordConfirm: null,
      token: null,
      new_password: null,

      showPwd: false,
      mode: 'login',
      loading: false,
      valid: false,
      loginRules: [required, email],
      modes: {
        signIn: 'login',
        signUp: 'register',
        forgot: 'forgot',
        forgotConfirm: 'forgotConfirm',
      },
      apiErrors: {
        password: null,
        email: null,
        username: null,
        token: null,
        new_password: null,
      },
    }
  },
  computed: {
    emailApiErrors() {
      if (this.apiErrors.username) {
        return this.apiErrors.username
      }
      return this.apiErrors.email
    },
    passwordRules() {
      const base = [required]
      if (this.mode === this.modes.signUp) {
        base.push(
          (v) => v === this.passwordConfirm || 'Password are not matching'
        )
      }
      return base
    },
    submitText() {
      if (this.mode === this.modes.signUp) {
        return 'Sign Up'
      }
      if (this.mode === this.modes.forgot) {
        return 'Send Recovery Email'
      }
      return 'Sign In'
    },
  },
  watch: {
    password() {
      this.validate()
    },
    passwordConfirm() {
      this.validate()
    },
    email() {
      this.resetApiError()
    },
  },
  methods: {
    loginUser() {
      this.$auth
        .loginWith('local', {
          data: {
            username: this.email,
            password: this.password,
          },
        })
        .catch((e) => {
          this.loading = false
          this.apiErrors.email = 'Login or password not correct'
        })
    },
    signUp() {
      this.$axios
        .$post('/api/auth/users/', {
          email: this.email,
          username: this.email,
          password: this.password,
        })
        .then(() => {
          this.$auth.loginWith('local', {
            data: {
              username: this.email,
              password: this.password,
            },
          })
        })
        .catch((e) => {
          this.loading = false
          if (e.response && e.response.data) {
            for (const property in e.response.data) {
              this.$set(this.apiErrors, property, e.response.data[property])
            }
          } else {
            this.apiErrors.email = 'Server error please try again later'
          }
        })
    },
    forgot() {
      this.$axios
        .$post('/api/auth/users/reset_password/', {
          email: this.email,
        })
        .then(() => {
          this.mode = this.modes.forgotConfirm
          this.loading = false
        })
        .catch((e) => {
          this.loading = false
          this.apiErrors.email = 'Server error please try again later'
        })
    },
    forgotConfirm() {},
    submitForm() {
      this.loading = true
      if (this.mode === this.modes.signIn) {
        this.loginUser()
      } else if (this.mode === this.modes.signUp) {
        this.signUp()
      } else if (this.mode === this.modes.forgot) {
        this.forgot()
      } else if (this.mode === this.modes.forgotConfirm) {
        this.forgotConfirm()
      }
    },
    switchMode(mode) {
      this.mode = mode
      this.resetValidation()
    },
    resetApiError() {
      for (const property in this.apiErrors) {
        this.$set(this.apiErrors, property, null)
      }
    },
    validate() {
      this.resetApiError()
      this.$refs.form.validate()
    },
    reset() {
      this.$refs.form.reset()
    },
    resetValidation() {
      this.$refs.form.resetValidation()
    },
  },
}
</script>
