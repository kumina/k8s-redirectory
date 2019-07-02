<template>
  <q-card>
    <q-item>
      <q-item-section avatar>
        <q-item-label caption>ID</q-item-label>
        <q-item-label>{{ domain.id }}</q-item-label>
      </q-item-section>

      <q-item-section>
        <q-item-label caption>RULE</q-item-label>
        <q-item-label>{{ domain.rule }}</q-item-label>
      </q-item-section>

      <q-item-section side top>
        <q-item-label caption> REGEX</q-item-label>
        <q-item-label :class="get_color(domain.is_regex)">{{ domain.is_regex }}</q-item-label>
      </q-item-section>
    </q-item>
  </q-card>
</template>

<script>
export default {
  name: 'DomainBlock',
  props: ['domain'],
  methods: {
    get_color (value) {
      if (value) {
        return 'text-green'
      } else {
        return 'text-red'
      }
    }
  }
}
</script>

<style scoped lang="stylus">
</style>
