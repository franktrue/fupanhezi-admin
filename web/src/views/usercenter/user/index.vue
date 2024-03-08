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
          <el-button size="small" type="primary" @click="addRow">
            <i class="el-icon-plus" /> 新增
          </el-button>
          <el-button size="small" type="success" :loading="loading" @click="dialogFormVisible = true">
            <i class="el-icon-qrcode" /> 小程序码
          </el-button>
          <el-button size="small" type="warning" :loading="loading" @click="dialogCouponFormVisible = true">
            <i class="el-icon-present" /> 发送优惠券
          </el-button>
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

    <el-dialog
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
      width="40%"
    >
      <template slot="title">
        小程序码 <small>参数自定义，需小程序端配合修改</small>
      </template>

      <el-form :model="fetchForm" ref="fetchForm" :rules="fetchFormRules">
        <el-form-item label="参数" prop="scene">
          <el-input
            v-model="fetchForm.scene"
          ></el-input>
        </el-form-item>
        <el-form-item label="页面" prop="page">
          <el-input
            v-model="fetchForm.page"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="fetchDataSubmit" :loading="loading">确定</el-button>
      </div>
      <el-image v-if="url.length > 0"
      style="width: 100px; height: 100px"
      :src="'data:image/png;base64,'+url"
      :fit="fit"></el-image>
    </el-dialog>

    <el-dialog
      :visible.sync="dialogCouponFormVisible"
      :close-on-click-modal="false"
      width="40%"
    >
      <template slot="title">
        发送优惠券
      </template>

      <el-form :model="couponForm" ref="couponForm" :rules="couponFormRules">
        <el-form-item label="优惠券场景ID" prop="couponSceneId">
          <el-input
            v-model="couponForm.couponSceneId"
          ></el-input>
          <span>请输入优惠券指定场景ID，提示：不是优惠券ID</span>
        </el-form-item>
        <el-form-item label="用户ID" prop="userId">
          <el-input
            v-model="couponForm.userId"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogCouponFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="userCouponSubmit" :loading="loading">确定</el-button>
      </div>
      <el-image v-if="url.length > 0"
      style="width: 100px; height: 100px"
      :src="'data:image/png;base64,'+url"
      :fit="fit"></el-image>
    </el-dialog>
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
      dialogFormVisible: false,
      dialogCouponFormVisible: false,
      loading: false,
      drawer: false,
      drawerWithdrawRecord: false,
      userRow: {},
      fetchForm: {
        scene: 'free_day=3&parent_id=',
        page: 'pages/tabbar-1/tabbar-1',
      },
      fetchFormRules: {
        scene: [
          { required: true, message: '必填项' }
        ]
      },
      couponForm: {
        couponSceneId: null,
        userId: null
      },
      url: ""
    }
  },
  methods: {
    fetchDataSubmit() {
      const that = this
      that.$refs.fetchForm.validate((valid) => {
        if (valid) {
          that.loading = true
          api.QrcodeObj(that.fetchForm).then((res) => {
            that.url = res.data
            that.loading = false
            that.$message.success('操作成功')
          }).catch(e => {
            that.loading = false
          })
        } else {
          that.$message.error('表单校验失败，请检查')
        }
      })
    },
    userCouponSubmit () {
      this.$refs.couponForm.validate((valid) => {
        if (valid) {
          this.loading = true
          api.SendCoupon(this.couponForm).then(res => {
            this.dialogCouponFormVisible = false
            this.$message.success('优惠券发送成功')
          }).catch(e => {
            this.loading = false
            this.$message.error(e.message)
          })
        } else {
          this.$message.error('表单校验失败，请检查')
        }
      })
    },
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
