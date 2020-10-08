<template>
  <div>
    <v-card class="py-8 px-6 pa-md-16">
      <v-form v-model="valid" ref="form" @submit.prevent="submitForm">
        <v-row class="flex-column-reverse flex-md-row">
          <v-col cols="12" md="6">
            <v-text-field
              v-model="email"
              :rules="loginRules"
              :error-messages="emailApiErrors"
              label="Email"
              required
              single-line
            ></v-text-field>
            <v-expand-transition>
              <v-text-field
                v-if="mode !== modes.forgot"
                v-model="pwd"
                :append-icon="showPwd ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPwd ? 'text' : 'password'"
                label="Password"
                :rules="passwordRules"
                :error-messages="apiErrors.password"
                @click:append="showPwd = !showPwd"
                required
                single-line
              ></v-text-field>
            </v-expand-transition>
            <v-expand-transition>
              <v-text-field
                v-if="mode === modes.signUp"
                v-model="pwdConfirm"
                type="password"
                :rules="passwordRules"
                label="Password Confirmation"
                single-line
              ></v-text-field>
            </v-expand-transition>

            <div class="d-flex pt-3 mb-5">
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
                  href="#"
                  @click="switchMode(modes.forgot)"
                  v-if="mode !== modes.forgot"
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
export default {
  layout: 'auth',
  data() {
    return {
      email: null,
      pwd: null,
      pwdConfirm: null,
      showPwd: false,
      mode: 'login',
      loading: false,
      valid: false,
      loginRules: [
        (v) => !!v || 'E-mail is required',
        (v) => /.+@.+/.test(v) || 'E-mail must be valid',
      ],
      modes: {
        signIn: 'login',
        signUp: 'register',
        forgot: 'forgot',
      },
      apiErrors: {
        password: null,
        email: null,
        username: null,
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
      const base = [(v) => !!v || 'Password is required']
      if (this.mode === this.modes.signUp) {
        base.push((v) => v === this.pwdConfirm || 'Password are not matching')
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
    pwd() {
      this.validate()
    },
    pwdConfirm() {
      this.validate()
    },
    email() {
      this.validate()
    },
  },
  methods: {
    loginUser() {
      this.$auth.loginWith('local', {
        data: {
          username: this.email,
          password: this.pwd,
        },
      })
    },
    async signUp() {
      try {
        const data = await this.$axios.$post('/api/auth/users/', {
          email: this.email,
          username: this.email,
          password: this.pwd,
        })
        this.$auth.loginWith('local', {
          data: {
            username: data.username,
            password: this.pwd,
          },
        })
      } catch (e) {
        if (e.response && e.response.data) {
          for (const property in e.response.data) {
            this.$set(this.apiErrors, property, e.response.data[property])
          }
        }
      }
    },
    forgot() {},
    submitForm() {
      this.loading = true
      if (this.mode === this.modes.signIn) {
        this.loginUser()
      } else if (this.mode === this.modes.signUp) {
        this.signUp()
      } else if (this.mode === this.modes.forgot) {
        this.forgot()
      }
      this.loading = false
    },
    switchMode(mode) {
      this.mode = mode
      this.resetValidation()
    },
    validate() {
      for (const property in this.apiErrors) {
        this.$set(this.apiErrors, property, null)
      }
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
