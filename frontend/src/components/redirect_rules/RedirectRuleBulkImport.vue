<template>
  <q-card id="create" class="my-card bg-grey-3 shadow-3">
    <q-card-section class="bg-primary text-white">
      <div class="row flex-center">
        <div class="col">
          <div class="text-h6">Bulk Import Redirect Rules</div>
        </div>
        <div class="col-auto">
          <q-icon name="cloud_upload" size="35px"/>
        </div>
      </div>
    </q-card-section>
    <q-separator class="toolbarGradient"/>

    <q-card-section>
      <q-card>
        <q-card-section>
          <div class="row">
            <div class="col-8">
              <p class="text-h4 row">
                Import from CSV file
              </p>
              <div class="doc-note">
                <p class="doc-note__title">QUICK TIP FOR SMOOTH IMPORT</p>
                <p>
                  Before bulk importing a CSV file please make sure that your CSV file
                  is in the correct format which is specified bellow.
                </p>
                <p>
                  A <b>boolean</b> can be represented by both an integer or a string.
                  Example: "1", "0", "true", "false"
                </p>
                <p>
                  Every cell has to be surrounded with "" (double clouts)
                </p>
              </div>
            </div>
            <div class="col" style="margin-left: 15px">
              <div class="row">
                <p class="col text-h4">
                  Upload
                </p>
                <p class="col-auto text-subtitle2 flex flex-center text-primary">
                  (drag and drop)
                </p>
              </div>
              <q-uploader
                :url="upload_url"
                :field-name="() => 'csv_file'"
                style="width: 100%;"
                label="Only CSV files">
                <template v-slot:header="scope">
                  <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
<!--                    <q-btn v-if="scope.queuedFiles.length > 0" icon="clear_all" @click="scope.removeQueuedFiles" round-->
<!--                           dense flat>-->
<!--                      <q-tooltip>Clear All</q-tooltip>-->
<!--                    </q-btn>-->
                    <q-btn v-if="scope.uploadedFiles.length > 0" icon="delete" @click="scope.removeUploadedFiles"
                           round dense flat>
                      <q-tooltip>Remove Uploaded Files</q-tooltip>
                    </q-btn>
                    <q-spinner v-if="scope.isUploading" class="q-uploader__spinner"/>
                    <div class="col">
                      <div class="q-uploader__title">Upload your files</div>
                      <div class="q-uploader__subtitle">{{ scope.uploadSizeLabel }} / {{ scope.uploadProgressLabel }}
                      </div>
                    </div>
                    <q-btn v-if="scope.editable && scope.queuedFiles.length < 1" icon="add_box" @click="scope.pickFiles"
                           label="PICK FILE" color="secondary">
                      <q-tooltip>Pick Files</q-tooltip>
                    </q-btn>
                    <q-btn v-if="scope.editable && scope.queuedFiles.length > 0" icon="cloud_upload"
                           @click="scope.upload" color="positive" label="UPLOAD FILE">
                      <q-tooltip>Upload Files</q-tooltip>
                    </q-btn>

                    <q-btn v-if="scope.editable && scope.isUploading" icon="clear" @click="scope.abort" round dense
                           flat>
                      <q-tooltip>Abort Upload</q-tooltip>
                    </q-btn>
                  </div>
                </template>
              </q-uploader>

            </div>
          </div>
          <br>
          <div class="row">
            <q-markup-table separator="cell" style="width: 100%">
              <tbody>
              <tr>
                <td>
                  <b>
                    Columns:
                  </b>
                </td>
                <td class="text-primary">domain</td>
                <td class="text-primary">domain_is_regex</td>
                <td class="text-primary">path</td>
                <td class="text-primary">path_is_regex</td>
                <td class="text-primary">destination</td>
                <td class="text-primary">destination_is_rewrite</td>
                <td class="text-primary">weight</td>
              </tr>
              <tr>
                <td>
                  <b>
                    Types:
                  </b>
                </td>
                <td class="text-primary">string</td>
                <td class="text-primary">boolean</td>
                <td class="text-primary">string</td>
                <td class="text-primary">boolean</td>
                <td class="text-primary">string</td>
                <td class="text-primary">boolean</td>
                <td class="text-primary">integer</td>
              </tr>
              <tr>
                <td>
                  <b>
                    Example 1:
                  </b>
                </td>
                <td>"test.com"</td>
                <td>"0"</td>
                <td>"/test/path.*"</td>
                <td>"1"</td>
                <td>"https://new_destination/new/path"</td>
                <td>"0"</td>
                <td>"100"</td>
              </tr>
              <tr>
                <td>
                  <b>
                    Example 2:
                  </b>
                </td>
                <td>".*\.test\.com"</td>
                <td>"true"</td>
                <td>"/bla/path"</td>
                <td>"false"</td>
                <td>"https://new_destination/bla/path"</td>
                <td>"false"</td>
                <td>"150"</td>
              </tr>
              </tbody>
            </q-markup-table>
          </div>
        </q-card-section>
      </q-card>
    </q-card-section>
    <q-separator class="separatorGradient"/>
  </q-card>
</template>

<script>
export default {
  name: 'RedirectRuleBulkImport',
  computed: {
    upload_url () {
      return this.$store.state.api.MGMT_RULES_BULK_IMPORT
    }
  },
  methods: {
    // upload (file) {
    //   let formData = new FormData()
    //   formData.append('csv_file', file[0])
    //
    //   this.$axios.post(this.$store.state.api.MGMT_RULES_BULK_IMPORT, formData, {
    //     headers: { 'Content-Type': 'multipart/form-data' } })
    //     .then(value => { return value })
    //     .catch(error => { return error })
    //
    //   return true
    // }
  }
}
</script>

<style lang="stylus" scoped>
  .my-card
    width 100%
</style>
