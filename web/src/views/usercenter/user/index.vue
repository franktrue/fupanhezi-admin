<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <!--    <template slot="header">测试页面1</template>-->
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @userAuth="userAuth"
      @userWithdrawRecord="userWithdrawRecord"
    >
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow"
            ><i class="el-icon-plus" /> 新增</el-button
          >
        </el-button-group>
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" />
      </div>
    </d2-crud-x>
    <el-drawer :visible.sync="drawer" :size="600">
      <div slot="title">
        <span>第三方登录信息</span>
        <el-tag size="small" style="margin-left: 10px">{{ userRow.nickname }}</el-tag>
      </div>
      <user-auth
        style="margin-top: 80px; margin-left: 10px"
        :userRow="userRow"
      >
      </user-auth>
    </el-drawer>
    <el-drawer :visible.sync="drawerWithdrawRecord" :size="800">
      <div slot="title">
        <span>提现记录</span>
        <el-tag size="small" style="margin-left: 10px">{{ userRow.nickname }}</el-tag>
      </div>
      <user-withdraw-record
        style="margin-top: 80px; margin-left: 10px"
        :userRow="userRow"
      >
      </user-withdraw-record>
    </el-drawer>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud' // 上文的crudOptions配置
import { d2CrudPlus } from 'd2-crud-plus'
import UserAuth from '@/views/usercenter/user/auth'
import UserWithdrawRecord from '@/views/usercenter/user/withdrawRecord'
export default {
  name: 'user',
  components: { UserAuth, UserWithdrawRecord },
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      loading: false,
      drawer: false,
      drawerWithdrawRecord: false,
      userRow: {}
    }
  },
  methods: {
    userAuth (scope) {
      this.drawer = true
      this.userRow = scope.row
    },
    userWithdrawRecord (scope) {
      this.drawerWithdrawRecord = true
      this.userRow = scope.row
    },
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      return api.GetList(query)
    },
    addRequest (row) {
      return api.createObj(row)
    },
    updateRequest (row) {
      return api.UpdateObj(row)
    },
    delRequest (row) {
      return api.DelObj(row.id)
    },
    /**
     * 懒加载
     * @param row
     * @returns {Promise<unknown>}
     */
    loadContentMethod ({ row }) {
      return new Promise(resolve => {
        api.GetList({ parent: row.id }).then(res => {
          resolve(res.data.data)
        })
      })
    }
  }
}
</script>

<style lang="scss">
.yxtInput {
  .el-form-item__label {
    color: #49a1ff;
  }
}
</style>
