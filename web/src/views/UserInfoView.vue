<script setup lang="ts">
import {useUserStore} from "@/stores/user.ts";

const userStore = useUserStore();

</script>

<template>
  <div>{{ userStore}}</div>
</template>

<style scoped>

</style>