<template>
  <q-card class="my-card bg-grey-3">
    <q-card-section class="bg-primary text-white">
      <div class="row flex-center">
        <div class="col">
          <div class="text-h6">Hyperscan Database and Workers</div>
        </div>
        <div class="col-auto">
          <q-icon name="group_work" size="35px"/>
        </div>
      </div>
    </q-card-section>
    <q-separator class="toolbarGradient"/>

    <q-card-section>
      <div class="row">
        <div class="col-auto" style="margin-right: 10px">
          <q-btn @click="compile_hs_db()" color="accent" icon="launch" label="COMPILE NEW HS DB"></q-btn>
        </div>
        <div class="col" style="margin-right: 10px">
          <q-btn @click="update_all_pods()" color="primary" icon="update" label="UPDATE ALL"></q-btn>
        </div>
        <div class="col-auto flex flex-center" style="margin-right: 10px">
          Refreshed: <b class="text-primary">&#160;{{ last_refreshed_seconds_ago }}s&#160;</b>
          ago.
        </div>
        <div class="col-auto">
          <q-btn @click="load_data()" round color="secondary" icon="refresh"></q-btn>
        </div>
      </div>
    </q-card-section>

    <q-card-section>
      <b class="text-h6">
        Management pod:
      </b>
      <div v-if="management_data !== null">
        <ManagementBlock :management-data="management_data"></ManagementBlock>
      </div>
      <div v-else>
        <div class="doc-note doc-note--warning">
          <p class="doc-note__title">Looks empty! How are you even loading this page??</p>
          <p>
            Check if you have configured the management pod with the right labels for the <i>"management_selector"</i> in the config.yaml
          </p>
        </div>
      </div>
    </q-card-section>

    <q-card-section>
      <b class="text-h6">
        Worker pods:
      </b>
      <div v-if="workers_data.length > 0">
        <WorkerBlock style="margin-top: 5px" class="col" :worker-data="worker" v-for="worker in workers_data"
                     v-bind:key="worker.pod.name"></WorkerBlock>
      </div>
      <div v-else>
        <div class="doc-note doc-note--warning">
          <p class="doc-note__title">No workers.. what do you mean?</p>
          <p>
            Check if you have configured the management pod with the right labels for the <i>"worker_selector"</i> in the config.yaml
          </p>
        </div>
      </div>
    </q-card-section>
    <q-separator class="separatorGradient"/>
  </q-card>
</template>

<script>
import WorkerBlock from '../blocks/WorkerBlock.vue'
import ManagementBlock from '../blocks/ManagementBlock.vue'

export default {
  name: 'Workers',
  components: {
    WorkerBlock, ManagementBlock
  },
  data () {
    return {
      management_data: null,
      workers_data: [],

      timer_update_data: null,
      timer_refresh_ago: null,
      timer_refresh_period: 1 * 10000,
      last_refreshed_time: null,
      last_refreshed_seconds_ago: null
    }
  },
  created () {
    this.load_data()

    // this.timer_update_data = setInterval(this.load_data, this.timer_refresh_period)
    // this.timer_refresh_ago = setInterval(this.update_refresh_time, 500)
  },
  beforeDestroy () {
    clearInterval(this.timer_update_data)
    clearInterval(this.timer_refresh_ago)
  },
  methods: {
    update_refresh_time () {
      const now = new Date()
      const seconds = (now.getTime() - this.last_refreshed_time) / 1000
      this.last_refreshed_seconds_ago = Math.round(seconds)
    },
    load_data () {
      this.$axios.get(this.$store.state.api.MGMT_KUBERNETES_GET_MANAGEMENT)
        .then((response) => {
          this.management_data = response.data.management
          console.log(this.management_data)
        })
        .catch((error) => {
          let errorData = error.response.data

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Unable to get management pod!\n' + errorData.error,
            icon: 'report_problem',
            actions: [{ icon: 'close', color: 'white' }]
          })
        })

      this.$axios.get(this.$store.state.api.MGMT_KUBERNETES_GET_WORKERS)
        .then((response) => {
          this.workers_data = response.data.workers
        })
        .catch((error) => {
          let errorData = error.response.data

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Unable to get worker pods!\n' + errorData.error,
            icon: 'report_problem',
            actions: [{ icon: 'close', color: 'white' }]
          })
        })

      this.last_refreshed_time = new Date()
    },
    update_all_pods () {
      this.update_management()
      this.update_workers()
    },
    update_workers () {
      this.$axios.get(this.$store.state.api.MGMT_DB_RELOAD_WORKERS)
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
        .catch()
    },
    update_management () {
      this.$axios.get(this.$store.state.api.MGMT_DB_RELOAD_MANAGEMENT)
        .then((response) => {
          let newVersion = response.data.new_hs_db_version

          this.$q.notify({
            color: 'green',
            position: 'top',
            message: 'New hyperscan db loaded: ' + newVersion,
            icon: 'check',
            actions: [{ icon: 'close', color: 'white' }]
          })
        })
        .catch((error) => {
          let message = error.response.data.error

          if (error.response.status === 404) {
            message = 'Unexpected error 404! Please check the connection to the server!'
          }

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: message,
            icon: 'report_problem',
            actions: [{ icon: 'close', color: 'white' }]
          })
        })
    },
    compile_hs_db () {
      this.$axios.get(this.$store.state.api.MGMT_DB_COMPILE)
        .then((response) => {
          let message = response.data.message

          this.$q.notify({
            color: 'green',
            position: 'top',
            message: message,
            icon: 'check',
            actions: [{ icon: 'close', color: 'white' }]
          })
        })
        .catch((error) => {
          let message = error.response.data.error

          if (error.response.status === 404) {
            message = 'Unexpected error 404! Please check the connection to the server!'
          }

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: message,
            icon: 'report_problem',
            actions: [{ icon: 'close', color: 'white' }]
          })
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
