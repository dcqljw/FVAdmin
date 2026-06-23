<!-- 登录页面 -->
<template>
  <div class="flex w-full h-screen">
    <LoginLeftView />

    <div class="relative flex-1">
      <AuthTopBar />

      <div class="auth-right-wrap">
        <div class="form">
          <h3 class="title">{{ $t('login.title') }}</h3>
          <p class="sub-title">{{ $t('login.subTitle') }}</p>
          <ElForm
            ref="formRef"
            :model="formData"
            :rules="rules"
            :key="formKey"
            @keyup.enter="handleSubmit"
            style="margin-top: 25px"
          >
            <!--            <ElFormItem prop="account">-->
            <!--              <ElSelect v-model="formData.account" @change="setupAccount">-->
            <!--                <ElOption-->
            <!--                  v-for="account in accounts"-->
            <!--                  :key="account.key"-->
            <!--                  :label="account.label"-->
            <!--                  :value="account.key"-->
            <!--                >-->
            <!--                  <span>{{ account.label }}</span>-->
            <!--                </ElOption>-->
            <!--              </ElSelect>-->
            <!--            </ElFormItem>-->
            <ElFormItem prop="username">
              <ElInput
                class="custom-height"
                :placeholder="$t('login.placeholder.username')"
                v-model.trim="formData.username"
              />
            </ElFormItem>
            <ElFormItem prop="password">
              <ElInput
                class="custom-height"
                :placeholder="$t('login.placeholder.password')"
                v-model.trim="formData.password"
                type="password"
                autocomplete="off"
                show-password
              />
            </ElFormItem>

            <!-- 验证码 -->
            <ElFormItem v-if="captchaEnabled" prop="captchaCode">
              <div class="captcha-row">
                <ElInput
                  class="custom-height captcha-input"
                  :placeholder="$t('login.placeholder.captcha')"
                  v-model.trim="formData.captchaCode"
                  autocomplete="off"
                  maxlength="6"
                />
                <div
                  class="captcha-img-wrap"
                  :title="$t('login.captchaRefresh')"
                  @click="loadCaptcha"
                >
                  <img v-if="captchaImage" :src="captchaImage" class="captcha-img" alt="captcha" />
                  <div v-else class="captcha-placeholder">
                    <span>{{ $t('login.captchaRefresh') }}</span>
                  </div>
                </div>
              </div>
            </ElFormItem>

            <!--            <div class="flex-cb mt-2 text-sm">-->
            <!--              <ElCheckbox v-model="formData.rememberPassword">{{-->
            <!--                $t('login.rememberPwd')-->
            <!--              }}</ElCheckbox>-->
            <!--              <RouterLink class="text-theme" :to="{ name: 'ForgetPassword' }">{{-->
            <!--                $t('login.forgetPwd')-->
            <!--              }}</RouterLink>-->
            <!--            </div>-->

            <div style="margin-top: 30px">
              <ElButton
                class="w-full custom-height"
                type="primary"
                @click="handleSubmit"
                :loading="loading"
                v-ripple
              >
                {{ $t('login.btnText') }}
              </ElButton>
            </div>

            <!--            <div class="mt-5 text-sm text-gray-600">-->
            <!--              <span>{{ $t('login.noAccount') }}</span>-->
            <!--              <RouterLink class="text-theme" :to="{ name: 'Register' }">{{-->
            <!--                $t('login.register')-->
            <!--              }}</RouterLink>-->
            <!--            </div>-->
          </ElForm>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import AppConfig from '@/config'
  import { useUserStore } from '@/store/modules/user'
  import { useI18n } from 'vue-i18n'
  import { HttpError } from '@/utils/http/error'
  import { fetchLogin, fetchCaptcha } from '@/api/auth'
  import { ElNotification, type FormInstance, type FormRules } from 'element-plus'
  import { initDynamicRoutes } from '@/router/guards/beforeEach'

  defineOptions({ name: 'Login' })

  const { t, locale } = useI18n()
  const formKey = ref(0)

  // 监听语言切换，重置表单
  watch(locale, () => {
    formKey.value++
  })

  type AccountKey = 'super' | 'admin' | 'user'

  export interface Account {
    key: AccountKey
    label: string
    userName: string
    password: string
    roles: string[]
  }

  const accounts = computed<Account[]>(() => [])

  const userStore = useUserStore()
  const router = useRouter()
  const route = useRoute()

  // 验证码相关
  const captchaEnabled = ref(false)
  const captchaKey = ref('')
  const captchaImage = ref('')

  const systemName = AppConfig.systemInfo.name
  const formRef = ref<FormInstance>()

  const formData = reactive({
    account: '',
    username: '',
    password: '',
    captchaCode: '',
    rememberPassword: true
  })

  const rules = computed<FormRules>(() => ({
    username: [{ required: true, message: t('login.placeholder.username'), trigger: 'blur' }],
    password: [{ required: true, message: t('login.placeholder.password'), trigger: 'blur' }],
    captchaCode: [{ required: true, message: t('login.placeholder.captcha'), trigger: 'blur' }]
  }))

  const loading = ref(false)

  onMounted(() => {
    setupAccount('super')
    loadCaptcha()
  })

  // 加载验证码
  const loadCaptcha = async () => {
    try {
      const res = await fetchCaptcha()
      captchaEnabled.value = true
      captchaKey.value = res.captchaKey
      captchaImage.value = res.image
    } catch {
      // 验证码未启用或请求失败，隐藏验证码区域
      captchaEnabled.value = false
    }
  }

  // 设置账号
  const setupAccount = (key: AccountKey) => {
    const selectedAccount = accounts.value.find((account: Account) => account.key === key)
    formData.account = key
    formData.username = selectedAccount?.userName ?? ''
    formData.password = selectedAccount?.password ?? ''
  }

  // 登录
  const handleSubmit = async () => {
    if (!formRef.value) return

    try {
      // 表单验证
      const valid = await formRef.value.validate()
      if (!valid) return

      loading.value = true

      // 构造登录参数
      const { username, password, captchaCode: code } = formData
      const loginParams: Api.Auth.LoginParams = { username, password }

      // 验证码启用时带上验证码参数
      if (captchaEnabled.value) {
        loginParams.captchaKey = captchaKey.value
        loginParams.captchaCode = code
      }

      const { token, refreshToken } = await fetchLogin(loginParams)

      // 验证token
      if (!token) {
        throw new Error('Login failed - no token received')
      }

      // 存储 token 和登录状态
      userStore.setToken(token, refreshToken)
      userStore.setLoginStatus(true)

      // 等待动态路由注册完成，确保跳转时路由已就绪
      await initDynamicRoutes(router)

      // 登录成功处理
      showLoginSuccessNotice()

      // 获取 redirect 参数，如果存在则跳转到指定页面，否则跳转到首页
      const redirect = route.query.redirect as string
      router.push(redirect || '/')
    } catch (error) {
      // 处理 HttpError
      if (error instanceof HttpError) {
        // 登录失败，刷新验证码
        if (captchaEnabled.value) {
          loadCaptcha()
        }
      } else {
        // 处理非 HttpError
        // ElMessage.error('登录失败，请稍后重试')
        console.error('[Login] Unexpected error:', error)
      }
    } finally {
      loading.value = false
    }
  }

  // 登录成功提示
  const showLoginSuccessNotice = () => {
    setTimeout(() => {
      ElNotification({
        title: t('login.success.title'),
        type: 'success',
        duration: 2500,
        zIndex: 10000,
        message: `${t('login.success.message')}, ${systemName}!`
      })
    }, 1000)
  }
</script>

<style scoped>
  @import './style.css';
</style>

<style lang="scss" scoped>
  :deep(.el-select__wrapper) {
    height: 40px !important;
  }

  .captcha-row {
    display: flex;
    width: 100%;
    gap: 10px;
  }

  .captcha-input {
    flex: 1;
  }

  .captcha-img-wrap {
    flex-shrink: 0;
    height: 40px;
    min-width: 120px;
    border-radius: calc(var(--custom-radius) / 3 + 2px);
    border: 1px solid var(--default-border);
    overflow: hidden;
    cursor: pointer;
    @apply tad-300;

    &:hover {
      border-color: var(--el-color-primary);
    }
  }

  .captcha-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .captcha-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: var(--art-gray-500);
  }
</style>
