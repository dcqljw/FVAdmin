<script setup lang="ts">
import {ref, reactive, onMounted} from 'vue';
import {userList} from "@/api/userApi.ts";
import {Icon} from "@iconify/vue";

const searchForm = reactive({
  username: '',
  phone: '',
  email: ''
})
const tableData = ref<any>([])
const showEditDialog = ref(false)

const searchHandle = () => {
  console.log(searchForm)
}

onMounted(() => {
  userList().then(res => {
    console.log(res)
    if (res.data.code === 200) {
      tableData.value.push(...res.data.data)
    }
    console.log(tableData)
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
        <el-button>添加用户</el-button>
      </div>
      <el-table :data="tableData">
        <el-table-column prop="username" label="用户名"/>
        <el-table-column prop="email" label="邮箱"/>
        <el-table-column label="状态"/>
        <el-table-column label="创建时间"/>
        <el-table-column fixed="right" label="操作">
          <template #default>
            <div class="flex gap-2">
              <el-tag type="primary" class="cursor-pointer" @click="showEditDialog = true">
                <Icon icon="ri:pencil-line" width="14" height="14"/>
              </el-tag>
              <el-tag type="danger" class="cursor-pointer">
                <Icon icon="ri:delete-bin-5-line" width="14" height="14"/>
              </el-tag>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div class="flex justify-center">
        <el-pagination
            :page-size="10"
            :page-count="100"
            layout="total, prev, pager, next"
        />
      </div>
    </el-card>
  </div>
  <el-dialog
      v-model="showEditDialog"
      title="编辑用户"
  >
    <el-form>
      <el-form-item label="用户名">
        <el-input/>
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input/>
      </el-form-item>
      <el-form-item label="角色">
        <el-input/>
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