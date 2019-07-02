<template>
  <div style="width: 100%">
    <q-card style="width: 100%" @mouseleave="lost_focus">
      <div class="row q-item cursor-pointer hoverable" @click="toggle_edit_mode" :class="is_dimmed">
        <div class="col-1">
          <q-item-label caption>ID</q-item-label>
          <q-item-label class="text-primary">{{ ambiguousRequest.id }}</q-item-label>
        </div>

        <div class="col">
          <q-item-label caption>REQUESTED URL</q-item-label>
          <q-item-label>{{ ambiguousRequest.request }}</q-item-label>
        </div>

        <div class="col-2">
          <q-item-label caption>CREATED AT</q-item-label>
          <q-item-label>{{ ambiguousRequest.created_at }}</q-item-label>
        </div>
      </div>
      <q-item v-show="edit_mode" class="absolute absolute-right overlay" style="width: 45%">
        <q-item-section>
          <div class="row" style="height: 100%">
            <div class="col flex flex-center">
              <q-btn @click="test_request" color="primary" unelevated class="edge-btn">
                <q-icon left name="visibility"/>
                <div>TEST REQUEST</div>
              </q-btn>
            </div>
            <div class="col flex flex-center">
              <q-btn @click="delete_ambiguous_request" color="negative" unelevated class="edge-btn">
                <q-icon left name="delete"/>
                <div>DELETE</div>
              </q-btn>
            </div>
          </div>
        </q-item-section>
      </q-item>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'AmbiguousBlock',
  props: ['ambiguousRequest'],
  data () {
    return {
      edit_mode: false
    }
  },
  computed: {
    is_dimmed () {
      return this.edit_mode ? 'dimmed' : ''
    }
  },
  methods: {
    toggle_configuration () {
      this.$store.commit('dialogs/set_configuration', this.managementData.status.configuration)
      this.$store.commit('dialogs/set_show_configuration', true)
    },
    toggle_edit_mode () {
      this.edit_mode = !this.edit_mode
    },
    lost_focus () {
      this.edit_mode = false
    },
    test_request () {
      this.$store.commit('mainPageView/setAmbiguousRequest', this.ambiguousRequest.request)
      this.$store.commit('mainPageView/setScrollTo', 'test_req')
    },
    delete_ambiguous_request () {
      let postData = {
        ambiguous_id: this.ambiguousRequest.id
      }

      this.$axios.post(this.$store.state.api.MGMT_AMBIGUOUS_DELETE, postData)
        .then(() => {
          this.$q.notify({
            color: 'green',
            position: 'top',
            message: 'Ambiguous request with id: ' + this.ambiguousRequest.id + ' has been deleted!',
            icon: 'check',
            actions: [{ icon: 'close', color: 'white' }]
          })

          this.$emit('reload')
        })
        .catch((error) => {
          let errorData = error.response.data

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: errorData.error,
            icon: 'report_problem',
            actions: [{ icon: 'close', color: 'white' }]
          })

          this.$emit('reload')
        })
    }
  }
}
</script>

<style lang="stylus" scoped>
  .mr-1
    margin-right 10px

  .edge-btn
    height 100%
    width 100%
    border-radius 0 !important
    opacity 0.9

  .overlay
    padding 0 !important

  .dimmed
    background: rgba(0, 0, 0, 0.5) !important;
</style>
