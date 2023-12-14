import moment from "moment"
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
      width: 280,
      fixed: 'right',
      custom: [{
        text: '使用场景',
        type: 'success',
        size: 'small',
        icon: 'el-icon-s-promotion',
        emit: 'couponScenes'
      }]

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
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '名称',
        key: 'name',
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        form: {
          rules: [
            { required: true, message: '请输入优惠券名称' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入优惠券名称'
          }
        }
      },
      {
        title: '优惠类型',
        key: 'type',
        type: 'radio',
        search: { disabled: false, component: { name: 'dict-select', props: { clearable: true } } },
        dict: {
          data: vm.dictionary('coupon_type')
        },
        form: {
          value: "full_reduction",
          component: {
            props: {
              clearable: true
            }
          },
          helper: "优惠类型",
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            if (value == "full_reduction") {
              getColumn('value').title = "金额"
              getColumn('value').helper = "满减填写额度"
            } else {
              getColumn('value').title = "百分点"
              getColumn('value').helper = "折扣填写百分点"
            }
          }
        }
      },
      {
        title: '金额/折扣',
        key: 'value',
        type: "number",
        form: {
          component: {
            name: 'el-input-number',
            props: {
              precision: 2
            }
          },
          // scopedSlots: {
          //   prefix: () => '￥'
          // },
          rules: [{ required: true, message: '必填' }],
          helper: "满减填写额度"
        }
      },
      {
        title: '最低使用金额',
        key: 'min_amount',
        type: "number",
        form: {
          component: {
            name: 'el-input-number',
            props: {
              precision: 2
            }
          },
          scopedSlots: {
            prefix: () => '￥'
          },
          rules: [{ required: true, message: '最小使用金额必填' }]
        }
      },
      {
        title: '有效期类型',
        key: 'expire_type',
        type: 'radio',
        search: { disabled: false, component: { name: 'dict-select', props: { clearable: true } } },
        dict: {
          data: vm.dictionary('expire_type')
        },
        form: {
          value: "countdown",
          component: {
            props: {
              clearable: true
            }
          },
          helper: "范围表示指定时间范围，倒计时表示领取后开始有效期天数",
        }
      },
      {
        title: '倒计时天数',
        key: 'days',
        type: "number",
        show: false,
        form: {
          component: {
            show (context) {
              const { form } = context
              return form.expire_type == "countdown"
            },
            name: 'el-input-number',
          },
          rules: [{ required: true, message: '天数必填' }]
        }
      },
      {
        title: "日期范围",
        key: "daterange",
        sortable: true,
        type: "daterange",
        show: false,
        form: {
          component: {
            show (context) {
              const { form } = context
              return form.expire_type == "range"
            },
            props: {
              "time-arrow-control": false,
              format: "yyyy-MM-dd",
              valueFormat: "yyyy-MM-dd",
            },
          },
          rules: [{ required: true, message: '天数必填' }]
        },
        valueBuilder(row, key) {
          if (row.expire_type == "range") {
            row.daterange = [
              row.start_time,
              row.end_time,
            ];
          } else {
            row.daterange = [
              moment().format('YYYY-MM-DD'),
              moment().add(1, 'years').format('YYYY-MM-DD'),
            ];
          }
        },
        valueResolve(row, key) {
          console.log(row)
          if (row.daterange != null && row.daterange.length > 1) {
            row.start_time = row.daterange[0];
            row.end_time = row.daterange[1];
          } else {
            row.start_time = moment().format('YYYY-MM-DD');
            row.end_time = moment().add(1, 'years').format('YYYY-MM-DD');
          }
        },
      },
      {
        title: '总数量',
        key: 'total_count',
        type: "number",
        form: {
          component: {
            name: 'el-input-number',
          },
          rules: [{ required: true, message: '总数量必填' }]
        }
      },
      {
        title: '说明',
        key: 'description',
        type: 'textarea',
        show: false,
        form: {
          component: {
            placeholder: '请输入说明',
            showWordLimit: true,
            maxlength: '500',
            props: {
              type: 'textarea'
            }
          }
        }
      },
      {
        title: '是否下架',
        key: 'status',
        type: 'dict-switch',
        dict: {
          data: vm.dictionary('button_whether_number')
        },
        form: {
          value: 0,
          component: {
            props: {
              clearable: true
            }
          },
          helper: "下架后不可用"
        }
      }
    ]
  }
}
