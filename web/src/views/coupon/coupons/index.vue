<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <!--    <template slot="header">测试页面1</template>-->
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @couponScenes="couponScenes"
    >
      <!-- 自动绑定参数与事件 -->
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
    <el-drawer :visible.sync="drawer" :size="700">
      <div slot="title">
        <span>使用场景</span>
        <el-tag size="small" style="margin-left: 10px">{{ subjectRow.name }}</el-tag>
      </div>
      <coupon-scenes
        style="margin-top: 80px; margin-left: 10px"
        :subjectRow="subjectRow"
      >
      </coupon-scenes>
    </el-drawer>
  </d2-container>
</template>

<script>
import { AddObj, GetList, UpdateObj, DelObj } from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import couponScenes from '@/views/coupon/coupons/scenes'
export default {
  name: 'Coupons',
  components: { couponScenes },
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      loading: false,
      drawer: false,
      subjectRow: {}
    }
  },
  methods: {
    couponScenes (scope) {
      this.drawer = true
      this.subjectRow = scope.row
    },
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      return GetList(query)
    }, // 数据请求
    addRequest (row) {
      return AddObj(row)
    }, // 添加请求
    updateRequest (row) {
      return UpdateObj(row)
    }, // 修改请求
    delRequest (row) {
      return DelObj(row.id)
    } // 删除请求
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
