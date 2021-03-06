<template>
  <div style="width: 100%">
    <q-card style="width: 100%" @mouseleave="lost_focus">
      <div class="row q-item cursor-pointer hoverable" @click="toggle_edit_mode" :class="is_dimmed">
        <div class="col-3">
          <q-item-label caption>NAME</q-item-label>
          <q-item-label class="text-primary">{{ workerData.pod.name }}</q-item-label>
        </div>

        <div class="col-1">
          <q-item-label caption>INTERNAL IP</q-item-label>
          <q-item-label>{{ workerData.pod.ip }}</q-item-label>
        </div>

        <div class="col">
          <q-item-label caption>PORT</q-item-label>
          <q-item-label>{{ workerData.pod.port }}</q-item-label>
        </div>

        <div class="col-1">
          <q-item-label caption>HEALTH</q-item-label>
          <q-item-label>
            <div v-if="workerData.status.health" class="text-positive text-bold">
              HEALTHY
            </div>
            <div v-else class="text-negative text-bold">
              UNHEALTHY
            </div>
          </q-item-label>
        </div>

        <div class="col-1">
          <q-item-label caption>READY</q-item-label>
          <q-item-label>
            <div v-if="workerData.status.ready" class="text-positive text-bold">
              READY
            </div>
            <div v-else class="text-negative text-bold">
              NOT READY
            </div>
          </q-item-label>
        </div>

        <div class="col-2">
          <q-item-label caption>HS DB VERSION</q-item-label>
          <q-item-label class="text-black">
            <div v-if="workerData.hyperscan.db_version !== null" class="text-positive text-bold">
              {{ workerData.hyperscan.db_version }}
            </div>
            <div v-else class="text-negative text-bold">
              UNKNOWN
            </div>
          </q-item-label>
        </div>
      </div>
      <q-item v-show="edit_mode" class="absolute absolute-right overlay" style="width: 45%">
        <q-item-section>
          <div class="row" style="height: 100%">
            <div class="col flex flex-center">
              <q-btn @click="toggle_configuration" color="primary" unelevated class="edge-btn">
                <q-icon left name="visibility"/>
                <div>VIEW CONFIGURATION</div>
              </q-btn>
            </div>
            <div class="col flex flex-center">
              <q-btn @click="update_worker" color="secondary" unelevated class="edge-btn">
                <q-icon left name="update"/>
                <div>RELOAD WORKERS DATABASES</div>
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
  name: 'WorkerBlock',
  props: ['workerData'],
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
      this.$store.commit('dialogs/set_configuration', this.workerData.status.configuration)
      this.$store.commit('dialogs/set_show_configuration', true)
    },
    toggle_edit_mode () {
      this.edit_mode = !this.edit_mode
    },
    lost_focus () {
      this.edit_mode = false
    },
    update_worker () {
      let postData = this.workerData.pod

      this.$axios.post(this.$store.state.api.MGMT_DB_RELOAD_WORKER, postData)
        .then((response) => {
          let respMessage = response.data.message

          this.$q.notify({
            color: 'green',
            position: 'top',
            message: respMessage,
            icon: 'check',
            actions: [{ icon: 'close', color: 'white' }]
          })
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
