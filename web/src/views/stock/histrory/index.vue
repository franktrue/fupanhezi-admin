<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <template slot="header">股票行情</template>
    <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners">
      <!-- 自动绑定参数与事件 -->
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow"><i class="el-icon-plus" /> 新增</el-button>
          <el-button size="small" type="warning" v-permission="'Fetch'" @click="dialogFormVisible = true"><i class="el-icon-refresh" /> 同步数据</el-button>
          <el-button size="small" type="success" v-permission="'FetchToday'" @click="fetchLatest" :loading="loading"><i class="el-icon-s-flag" /> 今日行情</el-button>
        </el-button-group>
        <crud-toolbar v-bind="_crudToolbarProps" v-on="_crudToolbarListeners" />
      </div>
    </d2-crud-x>

    <el-dialog
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
      width="40%"
    >
      <template slot="title">
        同步数据 <small>请确保股票代码及股票名称正确</small>
      </template>

      <el-form :model="fetchForm" ref="fetchForm" :rules="fetchFormRules" :inline="true">
        <el-form-item label="股票代码" prop="stock_code">
          <el-input
            v-model="fetchForm.stock_code"
          ></el-input>
        </el-form-item>
        <el-form-item label="股票名称" prop="stock_name">
          <el-input
            v-model="fetchForm.stock_name"
          ></el-input>
        </el-form-item>
        <el-form-item label="复权" prop="fq">
          <el-radio-group v-model="fetchForm.fq">
            <el-radio label="">不复权</el-radio>
            <el-radio label="qfq">前复权</el-radio>
            <el-radio label="hfq">后复权</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="时间范围" prop="between">
          <el-date-picker
            v-model="fetchForm.between"
            value-format="yyyy-MM-dd"
            type="daterange"
            :clearable="false"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期">
          </el-date-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="fetchDataSubmit" :loading="loading">确定</el-button>
      </div>
    </el-dialog>
  </d2-container>
</template>

<script>
import dayjs from 'dayjs'
import { crudOptions } from './crud' // 上文的crudOptions配置
import { d2CrudPlus } from 'd2-crud-plus'
import { AddObj, GetList, UpdateObj, DelObj, FetchData, UpdateLatest } from './api' // 查询添加修改删除的http请求接口
export default {
  name: 'stockHistory',
  mixins: [d2CrudPlus.crud], // 最核心部分，继承d2CrudPlus.crud
  data() {
    const startDate = dayjs('2020-01-01').format('YYYY-MM-DD')
    const endDate = dayjs().format('YYYY-MM-DD')
    return {
      dialogFormVisible: false,
      loading: false,
      fetchForm: {
        stock_code: null,
        stock_name: null,
        fq: 'qfq',
        between: [startDate, endDate]
      },
      fetchFormRules: {
        stock_code: [
          { required: true, message: '必填项' },
          {
            pattern: /^[0-9]{6}$/,
            message: '股票代码必须为6位数字',
            trigger: 'blur'
          }
        ],
        stock_name: [
          { required: true, message: '必填项' }
        ],
        between: [
          { required: true, message: '必填项' }
        ]
      }
    }
  },
  methods: {
    fetchDataSubmit() {
      const that = this
      that.$refs.fetchForm.validate((valid) => {
        if (valid) {
          that.loading = true
          FetchData(that.fetchForm).then((res) => {
            that.dialogFormVisible = false
            that.fetchForm = {
              stock_code: null,
              stock_name: null,
              between: []
            }
            that.daterange = [new Date(2020, 0, 1), new Date()]
            that.loading = false
            that.$message.success('操作成功')
            that.handleSearch()
          }).catch(e => {
            that.loading = false
          })
        } else {
          that.$message.error('表单校验失败，请检查')
        }
      })
    },
    // 获取最新股票行情
    fetchLatest() {
      const that = this
      this.$confirm('今日行情必须在每个交易日15点以后更新，是否确认更新?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        that.loading = true
        return UpdateLatest().then(res => {
          that.loading = false
          that.$message.success('操作成功')
          that.handleSearch()
        })
      })
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
