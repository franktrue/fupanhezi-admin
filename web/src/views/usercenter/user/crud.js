export const crudOptions = (vm) => {
  return {
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
      width: 400,
      fixed: 'right',
      custom: [
        {
          text: '提现记录',
          type: 'danger',
          size: 'small',
          icon: 'el-icon-money',
          emit: 'userWithdrawRecord'
        },
        {
          text: '第三方登录信息',
          type: 'success',
          size: 'small',
          icon: 'el-icon-folder',
          emit: 'userAuth'
        },
      ]

    },
    indexRow: false,
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
        width: 60,
        search: true,
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '上级ID',
        key: 'parent_id',
        show: false,
        search: true,
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
      },
      {
        title: '邀请数量',
        key: 'has_children',
        form: {
          component: {
            show: false
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
            show: false
          }
        }
      },
      {
        title: '总佣金',
        key: 'reward_amount',
        type: 'number',
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '已提现',
        key: 'withdraw_amount',
        type: 'number',
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '分佣信息',
        key: 'reward_info',
        width: 120,
        type: 'text',
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '分佣类型',
        key: 'reward_type',
        type: 'radio',
        show: false,
        dict: {
          data: vm.dictionary('reward_type')
        },
        form: {
          value: 'percent',
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            if (value == 'percent') {
              getColumn('reward_value').title = '百分比%'
              getColumn('reward_value').component.placeholder = '请输入百分点'
              getColumn('reward_value').helper = "分佣时按照成交百分点计算"
            } else {
              getColumn('reward_value').title = '固定额度¥'
              getColumn('reward_value').component.placeholder = '请输入金额'
              getColumn('reward_value').helper = "分佣时奖励固定金额"
            }
          }
        }
      },
      {
        title: '分佣值',
        key: 'reward_value',
        type: 'number',
        show: false,
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '必填项' }
          ],
          value: 30,
          component: {
            name: 'el-input-number',
            props: {
              precision: 2
            }
          },
          helper: "分佣时按照成交百分点计算"
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
        title: '最后登录时间',
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
