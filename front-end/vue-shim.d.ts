import Auth from '@nuxtjs/auth/lib/core/auth'
import Vue from 'vue'

declare module 'vue/types/vue' {
  interface Vue {
    $auth: Auth
  }
}

declare module '*.vue' {
  import Vue from 'vue'
  export default Vue
}
