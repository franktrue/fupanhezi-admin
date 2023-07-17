<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <!--    <template slot="header">测试页面1</template>-->
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @userAuth="userAuth"
    >
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button
            size="small"
            v-permission="'Create'"
            type="primary"
            @click="addRow"
            ><i class="el-icon-plus" /> 新增</el-button
          >
        </el-button-group>
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
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
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import UserAuth from '@/views/usercenter/user/auth'
export default {
  name: 'user',
  components: { UserAuth },
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      loading: false,
      drawer: false,
      userRow: {}
    }
  },
  methods: {
    userAuth (scope) {
      this.drawer = true
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
