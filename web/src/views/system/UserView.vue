<script setup lang="ts">
import {ref, reactive, onMounted} from 'vue';
import {userList} from "@/api/userApi.ts";
import {getRoleList} from "@/api/roleApi.ts";

const searchForm = reactive({
  username: '',
  phone: '',
  email: ''
})
const usersData = ref<any>([])
const usersTotal = ref(0)
const currentUser = ref<any>({})
const roleList = ref<any>([])
const showEditDialog = ref(false)
const showUserInfoDialog = ref(false)
const cacheUser = ref<any>({})

const searchHandle = () => {
  console.log(searchForm)
}

const closeEditDialogHandle = () => {
  console.log("closeEditDialogHandle")
  cacheUser.value = {}
  console.log(cacheUser.value)
}

onMounted(() => {
  userList().then(res => {
    console.log(res)
    if (res.data.code === 200) {
      console.log(res.data.data)
      usersData.value.push(...res.data.data.users)
      usersTotal.value = res.data.data.total
    }
    console.log(usersData)
  })
  getRoleList().then(res => {
    console.log(res)
    if (res.data.code === 200) {
      roleList.value.push(...res.data.data)
    }
  })
})
</script>

<template>
  <div class="flex flex-col gap-4">
    <el-card shadow="never">
      <el-form :inline="true" :rules="searchForm">
        <el-form-item label="用户名" class="!mb0">
          <el-input v-model="searchForm.username"/>
        </el-form-item>
        <el-form-item label="手机号" class="!mb0">
          <el-input v-model="searchForm.phone"/>
        </el-form-item>
        <el-form-item label="邮箱" class="!mb0">
          <el-input v-model="searchForm.email"/>
        </el-form-item>
        <el-form-item class="!mb0">
          <el-button type="primary" @click="searchHandle">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card shadow="never">
      <div>
        <el-button type="primary">新增</el-button>
      </div>
      <el-table :data="usersData">
        <el-table-column label="序号" width="80">
          <template #default="scope">
            {{ scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="昵称">
          <template #default="{row}">
            <div class="flex items-center gap-2">
              <el-avatar>{{ row.nickname.slice(0, 2) }}</el-avatar>
              <span>{{ row.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="100"/>
        <el-table-column prop="email" label="邮箱"/>
        <el-table-column label="状态">
          <template #default="{row}">
            <el-tag v-if="row.status === 1" type="success">正常</el-tag>
            <el-tag v-else type="danger">禁用</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间"/>
        <el-table-column fixed="right" label="操作">
          <template #default="{row}">
            <div class="flex gap-2">
              <el-link type="primary" @click="showUserInfoDialog = true;currentUser=row">详情</el-link>
              <el-link type="primary" @click="showEditDialog = true;cacheUser={...row}">修改</el-link>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div class="flex justify-center">
        <el-pagination
            :total="usersTotal"
            layout="total, prev, pager, next"
        />
      </div>
    </el-card>
  </div>
  <el-dialog
      v-model="showUserInfoDialog"
      title="详情"
      width="500"
  >
    <el-descriptions
        :column="2"
        label-width="60"
    >
      <el-descriptions-item label="ID" :span="2">{{ currentUser.id }}</el-descriptions-item>
      <el-descriptions-item label="用户名">{{ currentUser.username }}</el-descriptions-item>
      <el-descriptions-item label="昵称">{{ currentUser.nickname }}</el-descriptions-item>
      <el-descriptions-item label="邮箱">{{ currentUser.email }}</el-descriptions-item>
      <el-descriptions-item label="状态">
        <el-tag v-if="currentUser.status" type="success">正常</el-tag>
        <el-tag v-else type="danger">禁用</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="角色" :span="2">
        <el-tag v-for="i in currentUser.roles">
          {{ i }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="创建时间" :span="2">{{ currentUser.created_at }}</el-descriptions-item>
    </el-descriptions>
  </el-dialog>
  <el-dialog
      v-model="showEditDialog"
      title="编辑用户"
      @close="closeEditDialogHandle"
      :align-center="true"
      width="500"
  >
    <el-form label-width="auto">
      <el-form-item label="用户名">
        <el-input v-model="cacheUser.username"/>
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input/>
      </el-form-item>
      <el-form-item label="角色">
        <el-select
            v-model="cacheUser.roles"
            multiple
            placeholder="请选择角色"
        >
          <el-option
              v-for="item in roleList"
              :key="item.id"
              :label="item.name"
              :value="item.name"
          >
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="showEditDialog = false">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>

</style>