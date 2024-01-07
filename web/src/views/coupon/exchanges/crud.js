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
        text: '兑换码',
        type: 'success',
        size: 'small',
        icon: 'el-icon-s-promotion',
        emit: 'exchangeCodes'
      }]

    },
    indexRow: false,
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 24, // 默认的表单 span
      width: "900px"
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
            { required: true, message: '请输入使用场景名称' }
          ],
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入名称',
          }
        }
      },
      {
        title: '类型',
        key: 'type',
        type: 'radio',
        search: { disabled: false, component: { name: 'dict-select', props: { clearable: true } } },
        dict: {
          data: vm.dictionary('coupon_exchange_type')
        },
        form: {
          value: "only",
          component: {
            props: {
              clearable: true
            }
          },
          helper: "通用码可使用多次，单次码需手动再次生成",
        },
        valueBuilder(row, key) {
          if (row.type == "many") {
            row.expire_type = "range"
          }
        },
      },
      {
        title: '兑换码',
        key: 'code',
        type: 'input',
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        width: 120,
        form: {
          component: {
            show: false
          }
        },
        formatter: (row, column, cellValue) => {
          if (row.type == "many") {
            return cellValue
          } else {
            return ""
          }
        },
      },
      {
        title: '有效期 年',
        key: 'year_num',
        type: 'number',
        width: 100,
        form: {
          value: 0,
          component: {
            span: 8,
            props: {
              clearable: true
            }
          },
          rules: [{ required: true, message: '有效期必填' }]
        }
      },
      {
        title: '月',
        key: 'month_num',
        type: 'number',
        width: 60,
        form: {
          value: 0,
          component: {
            span: 8,
            props: {
              clearable: true
            }
          },
          rules: [{ required: true, message: '有效期必填' }]
        }
      },
      {
        title: '日',
        key: 'day_num',
        type: 'number',
        width: 60,
        form: {
          value: 0,
          component: {
            span: 8,
            props: {
              clearable: true
            }
          },
          rules: [{ required: true, message: '有效期必填' }]
        }
      },
      {
        title: '对应等级',
        key: 'level',
        type: "number",
        form: {
          value: 1,
          component: {
            name: 'el-input-number',
          },
          rules: [{ required: true, message: '对应等级必填' }],
          helper: "用户默认等级为1级"
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
        show: false,
        form: {
          value: "countdown",
          component: {
            show (context) {
              const { form } = context
              return form.type == "only"
            },
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
              return form.expire_type == "countdown" && form.type == "only"
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
              return form.expire_type == "range" || form.type == "many"
            },
            props: {
              "time-arrow-control": false,
              format: "yyyy-MM-dd",
              valueFormat: "yyyy-MM-dd",
            },
          },
          rules: [{ required: true, message: '日期范围必填' }]
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
            props: {
              clearable: true
            }
          },
          helper: "单次码建议小于1000个"
        },
      },
      {
        title: '已使用',
        key: 'used_count',
        type: "number",
        form: {
          component: {
            show: false
          }
        }
      },
      {
        title: '是否下架',
        key: 'del_flag',
        type: 'dict-switch',
        dict: {
          data: vm.dictionary('button_whether_bool')
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
    ].concat(vm.commonEndColumns())
  }
}
