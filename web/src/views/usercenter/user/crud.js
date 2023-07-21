import { request } from '@/api/service'
import { urlPrefix as subjectPrefix } from './api'
import XEUtils from 'xe-utils'
export const crudOptions = (vm) => {
  return {
    pagination: false,
    pageOptions: {
      compact: true
    },
    options: {
      tableType: "vxe-table",
      rowKey: true, // 必须设置，true or false
      rowId: "id",
      height: "100%", // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false
    },
    rowHandle: {
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      },
      width: 280,
      fixed: 'right',
      custom: [{
        text: '第三方登录信息',
        type: 'success',
        size: 'small',
        icon: 'el-icon-folder',
        emit: 'userAuth'
      }]

    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 80
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 24, // 默认的表单 span
      width: "35%"
    },
    columns: [
      {
        title: 'ID',
        key: 'id',
        show: false,
        width: 60,
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '昵称',
        key: 'nickname',
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        form: {
          component: {
            props: {
              elProps: {
                clearable: true,
                showAllLevels: false, // 仅显示最后一级
                props: {
                  checkStrictly: true, // 可以不需要选到最后一级
                  emitPath: false,
                  clearable: true
                }
              }
            },
            placeholder: '请输入昵称'
          },
        },
        editForm: {
          component: {
            readonly: true
          }
        }
      },
      {
        title: '手机号',
        key: 'mobile',
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        form: {
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入手机号'
          }
        }
      },
      {
        title: '有效期',
        key: 'expire_time',
        sortable: true,
        type: 'datetime',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '有效期必填项' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入有效期'
          },
        }
      },
      {
        title: '更新时间',
        key: 'update_time',
        sortable: true,
        type: 'datetime',
        form: {
          disabled: true
        }
      },
      {
        title: '注册时间',
        key: 'create_time',
        sortable: true,
        type: 'datetime',
        form: {
          disabled: true
        }
      },
    ]
  }
}
