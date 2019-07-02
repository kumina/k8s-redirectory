<template>
  <!--hHh Lpr lff-->
  <q-layout view="hHh Lpr lFf">
    <q-ajax-bar
      ref="bar"
      position="top"
      color="secondary"
      size="3px"
    />
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round @click="toggleDrawer()" aria-label="Menu">
          <q-icon name="menu"/>
        </q-btn>

        <q-toolbar-title>
          Redirectory
        </q-toolbar-title>

        <div>
          <q-btn flat class="bg-info text-white" v-ripple @click="openURL('https://www.kumina.nl')">
            Kumina B.V.
          </q-btn>
        </div>
      </q-toolbar>
      <div class="toolbarGradient">
      </div>
    </q-header>

    <q-drawer
      :mini="isDrawerMenuMini"
      @mouseover="miniState = false"
      @mouseout="miniState = true"
      :width="225"
      :breakpoint="500"
      show-if-above
      bordered
      content-class="bg-grey-3"
    >
      <q-scroll-area class="fit">
        <q-list padding>
          <q-item clickable v-ripple @click="scrollTo('test_req')">
            <q-item-section avatar>
              <q-icon name="http" color="primary"/>
            </q-item-section>
            <q-item-section>
              Test request
            </q-item-section>
          </q-item>

          <q-item-label header>Redirect Rules</q-item-label>
          <q-separator class="separatorGradient"/>

          <q-item clickable v-ripple @click="scrollTo('rr_search')">
            <q-item-section avatar>
              <q-icon name="explore" color="primary"/>
            </q-item-section>
            <q-item-section>
              Rule Explorer | Editor
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="scrollTo('rr_bulk')">
            <q-item-section avatar>
              <q-icon name="cloud_upload" color="primary"/>
            </q-item-section>
            <q-item-section>
              Bulk Import
            </q-item-section>
          </q-item>

          <q-item-label header>Inner Workings</q-item-label>
          <q-separator class="separatorGradient"/>
          <q-item clickable v-ripple @click="scrollTo('iw_worker')">
            <q-item-section avatar>
              <q-icon name="group_work" color="primary"/>
            </q-item-section>
            <q-item-section>
              HS DB and Workers
            </q-item-section>
          </q-item>
          <q-item clickable v-ripple @click="scrollTo('iw_amb_req')">
            <q-item-section avatar>
              <q-icon name="report" color="primary"/>
            </q-item-section>
            <q-item-section>
              Ambiguous requests
            </q-item-section>
          </q-item>

          <q-item-label header>Other</q-item-label>
          <q-separator class="separatorGradient"/>
          <q-item clickable v-ripple @click="openUserGuideDialog()">
            <q-item-section avatar>
              <q-icon name="school" color="primary"/>
            </q-item-section>
            <q-item-section>
              User Guide
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="openURL(api_doc_url)">
            <q-item-section avatar>
              <q-icon name="apps" color="primary"/>
            </q-item-section>
            <q-item-section>
              Api
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>
</template>

<script>
import { openURL, scroll } from 'quasar'

const { getScrollTarget, setScrollPosition } = scroll

export default {
  name: 'MainPageLayout',
  data () {
    return {
      leftDrawerOpen: this.$q.platform.is.desktop,
      drawer: true,
      miniState: true
    }
  },
  watch: {
    scroll_to (newVal, oldVal) {
      if (newVal === null) {
        return
      }

      this.scrollTo(newVal)
      this.$store.commit('mainPageView/setScrollTo', null)
    }
  },
  computed: {
    isDrawerMenuMini () {
      return this.drawer === true ? false : this.miniState
    },
    api_doc_url () {
      return this.$store.state.api.API_DOC_URL
    },
    scroll_to () {
      return this.$store.state.mainPageView.scrollTo
    }
  },
  methods: {
    openURL,
    toggleDrawer () {
      this.drawer = !this.drawer
    },
    sleep (ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    async scrollTo (id) {
      if (id.startsWith('rr')) {
        this.$store.commit('mainPageView/setRedirectRuleOpened', true)
      } else if (id.startsWith('iw')) {
        this.$store.commit('mainPageView/setInnerWorkingsOpened', true)
      }

      this.$store.commit('mainPageView/setRipple', true)
      await this.sleep(100)

      let element = document.getElementById(id)
      let offset = getScrollTarget(element).offsetTop + element.offsetTop
      setScrollPosition(window, offset, 100)
      element.click()
      this.$store.commit('mainPageView/setRipple', false)
    },
    openUserGuideDialog () {
      this.$store.commit('dialogs/set_user_guide', true)
    }
  }
}
</script>

<style lang="stylus">
  .vjs-value__string
    color: $accent !important
</style>
