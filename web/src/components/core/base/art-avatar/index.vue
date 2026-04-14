<!-- 头像组件：显示首字母大写 + 随机背景色 -->
<template>
  <div
    class="art-avatar flex-cc rounded-full font-medium shrink-0"
    :style="avatarStyle"
  >
    <template v-if="src">
      <img :src="src" alt="avatar" class="w-full h-full rounded-full object-cover" />
    </template>
    <template v-else>
      <span class="avatar-text">{{ initials }}</span>
    </template>
  </div>
</template>

<script setup lang="ts">
  defineOptions({ name: 'ArtAvatar' })

  interface Props {
    /** 头像图片路径，未传则显示首字母 */
    src?: string
    /** 用于生成首字母的文本（如用户名） */
    name?: string
    /** 头像大小（像素），默认 34 */
    size?: number
  }

  const props = withDefaults(defineProps<Props>(), {
    src: '',
    name: '',
    size: 34
  })

  // 生成首字母
  const initials = computed(() => {
    if (!props.name) return '?'
    return props.name.charAt(0).toUpperCase()
  })

  // 根据名称生成稳定的背景色（哈希取色）
  const avatarColor = computed(() => {
    const name = props.name || '?'
    const colors = [
      '#5B8FF9', // 蓝
      '#5AD8A6', // 绿
      '#5D7092', // 灰蓝
      '#F6BD16', // 黄
      '#E8684A', // 橙红
      '#6DC88A', // 浅绿
      '#FF99C3', // 粉
      '#269AFA', // 天蓝
      '#9270CA', // 紫
      '#FF9D4D'  // 橙
    ]
    let hash = 0
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash)
    }
    return colors[Math.abs(hash) % colors.length]
  })

  const avatarStyle = computed(() => ({
    width: `${props.size}px`,
    height: `${props.size}px`,
    backgroundColor: props.src ? undefined : avatarColor.value,
    fontSize: `${props.size * 0.45}px`
  }))
</script>

<style scoped lang="scss">
  .art-avatar {
    overflow: hidden;
    color: #fff;

    .avatar-text {
      user-select: none;
      line-height: 1;
    }
  }
</style>
