<template>
  <q-card class="my-card bg-grey-3">
    <q-card-section class="bg-primary text-white">
      <div class="row flex-center">
        <div class="col">
          <div class="text-h6">Ambiguous Requests</div>
        </div>
        <div class="col-auto">
          <q-icon name="report" size="35px"/>
        </div>
      </div>
    </q-card-section>
    <q-separator class="toolbarGradient"/>

    <q-card-section>
      <div class="row">
        <div class="col-auto text-h4 flex flex-center">
          List
        </div>
        <div class="col">
        </div>
        <div class="col-auto">
          <q-btn @click="load_ambiguous_requests()" color="secondary" icon="refresh" label="RELOAD AMBIGUOUS REQUESTS"></q-btn>
        </div>
      </div>
    </q-card-section>

    <q-card-section>
      <div v-if="is_loaded">
        <AmbiguousBlock style="margin-top: 5px" :ambiguous-request="ambiguous_request"
                        v-for="ambiguous_request in ambiguous_requests"
                        v-bind:key="ambiguous_request.id"
                        v-on:reload="load_ambiguous_requests"></AmbiguousBlock>
      </div>
      <div v-if="ambiguous_requests === null">
        <div class="doc-note doc-note--tip">
          <p class="doc-note__title">Looks empty!</p>
          <p>
            Great job, seems like all the rules are properly configured.
          </p>
        </div>
      </div>
    </q-card-section>
    <q-separator class="separatorGradient"/>
  </q-card>
</template>

<script>
import AmbiguousBlock from '../blocks/AmbiguousBlock.vue'

export default {
  name: 'AmbiguousRequests',
  components: {
    AmbiguousBlock
  },
  data () {
    return {
      ambiguous_requests: null,
      is_loaded: false
    }
  },
  created () {
    this.load_ambiguous_requests()
  },
  methods: {
    load_ambiguous_requests () {
      this.$axios.get(this.$store.state.api.MGMT_AMBIGUOUS_LIST)
        .then((response) => {
          this.ambiguous_requests = response.data.ambiguous_requests
          this.is_loaded = true
        })
        .catch(() => {
          this.ambiguous_requests = null
        })
    }
  }
}
</script>

<style lang="stylus" scoped>
  .my-card
    width 100%

  /*max-width 1800px*/
  /*margin-left 5%*/
  /*margin-right 5%*/
</style>
