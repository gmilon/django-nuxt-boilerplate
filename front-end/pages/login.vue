<template>
  <div>
    <v-card class="py-8 px-6 pa-md-16">
      <form @submit.prevent="submitForm">
        <v-row class="flex-column-reverse flex-md-row">
          <v-col cols="12" md="6" class="d-flex flex-column justify-center">
            <v-text-field
              v-model="login"
              label="Email"
              single-line
            ></v-text-field>
            <v-expand-transition>
              <v-text-field
                v-if="mode !== modes.forgot"
                v-model="pwd"
                label="Password"
                single-line
              ></v-text-field>
            </v-expand-transition>
            <v-expand-transition>
              <v-text-field
                v-if="mode === modes.signUp"
                v-model="pwd"
                label="Password Confirmation"
                single-line
              ></v-text-field>
            </v-expand-transition>

            <div class="d-flex mt-3 mb-5">
              <v-btn
                v-if="mode === modes.signIn"
                type="submit"
                large
                block
                :loading="loading"
              >
                Sign In
              </v-btn>
              <v-btn
                v-else-if="mode === modes.signUp"
                type="submit"
                block
                large
                :loading="loading"
              >
                Sign Up
              </v-btn>
              <v-btn
                v-else-if="mode === modes.forgot"
                type="submit"
                block
                large
                :loading="loading"
              >
                Send email
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
      </form>
    </v-card>
  </div>
</template>

<script>
export default {
  layout: 'auth',
  data() {
    return {
      login: null,
      pwd: null,
      pwdConfirm: null,
      mode: 'login',
      loading: false,
      modes: {
        signIn: 'login',
        signUp: 'register',
        forgot: 'forgot',
      },
    }
  },
  methods: {
    loginUser() {
      this.$auth.loginWith('local', {
        data: {
          username: this.login,
          password: this.pwd,
        },
      })
    },
    signUp() {},
    forgot() {},
    submitForm() {
      this.loading = true
      if (this.mode === this.modes.signIn) {
        this.loginUser()
      } else if (this.mode === this.modes.regiser) {
        this.signUp()
      } else if (this.mode === this.modes.forgot) {
        this.forgot()
      }
      this.loading = false
    },
    switchMode(mode) {
      this.mode = mode
    },
  },
}
</script>
