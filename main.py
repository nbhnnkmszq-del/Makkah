import base64
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# ============================================================
# 1. تحديث حوض البيانات النظيفة المستخرجة من الآيفون 7 (iOS 15.8.6)
# ============================================================
IPHONE7_CLEAN_POOL = {
    # المعرف الفرعي الحقيقي المستخرج من الـ Logs
    "device_uuid": "0196B3EE-508D-4FAC-9F7B-1B790E57DDBB",
    
    # توكن الوصول الأساسي المستخرج حديثاً
    "access_token": "hCgwKCjE3Nzk2NzA4MjASgAHPo67ALSrMM9NeAahNE3jdlHSkQ-UzFQdCMXtlsYfixAZXA7omp_H7jlk",
    "access_token_alt": "gEgIIARrGASHYUNaM8ScYAmymOmpHjoCXlPjPVLOO9p0aRI-wVSJSE3n72FT24W5ngP4eFA3uLaOVuHV",
    
    # توكن التحقق ومكافحة التلاعب (Attestation Token) الصادر من الجهاز النظيف
    "att_token": "Ci1iNFCsaIvuN4FmwoMSXqFN1o531mchZS20Zbt9Sv2TDy8ACaUEsYDd88NjSwoVAQAAAA==",
    "user_id": "55a118bf-16cd-4527-9ea7-9f90fdab8faf",
    
    # مصفوفة الـ Protobuf الرئيسية المستخرجة من الآيفون 7 بالكامل
    "protobuf_base64_payload": "AgAAALNM08/993DBeA8N2fljKBoEUNk0+me89vLfv5ZingpyOOkgXXXyjPzYTzWmWSu+BYqcD47byirLZ++3dJccpF99hWppT7G5xAuU+y56WpSYsARYCqnfnV6E0RogQbB/S5gJg3fdrGK281whhCzVXeVpFBjl/vz/UCggfHsMJXwzqN23CjPgisuDGuOx0xQuEozpVAgAAEj2/BE6mQXYMruHN/C9kv+lzKC6NJo7r9bjTsSCVizujZSB8koUpmNodQXYZvbQBKCVP+tggjJOsHSjqU+zY2+sb+DrMOUe3rGAqoFMXUydxwYQmLYZz4VdnTVCDtNKIZ9HNX3wEmR+NDSQBNYhIiJgX29z1WzlasSKfaup9zt7i19Pqetg3dGNepXnl8f0cComMsdrAyEHKuRbdWfMjXmzmZiElf4GEPUyWPpan7p/ljfAJGvMDaZR0bE5SccIWnt45GFeoqYei456D5234zsBGW8nLgX8ZCyDtUbitDwuO8lQLYqg3Vl7zwJl6adn7UguSSgr3LWywDgQs8W8wRMluXPI3/R9Fqx8NNkwu/OQH0GFKRK249Tqz03l0kPvu/iw/qfm0umMNRbsmj9StdcKJxmsFsJ7njB72ef/oH2jmIQVeaURY7RElfRA8ZgXjbIs/CqTj+WvdIah17XOqkfmMD0/RlO3TOcgfiCTuUaVPKcDWvJVaWr1fLfkSjTW2HyL3FXYzJoOYmjQS6aMM7uzu5IA5E5d0RguFnjj5eHOiXzCeszBkGMc2eOO9x59YJ9DfYZwk9Z8bm3ji1/U4QAHAObspPL+tbLD3Mo+McTzHCZYUC8VJ5D6m5P9DiWcdCB9DowELw3Ow2P0Xgck1E0LDqkFxLjNJu30Uq+3YdiVbmcPEYhsQtiT9cuQAcigKPWd9Kmi689/QMINktn4nUVQJDtVl4ETGKtRjnXUcijRLnyAqJTMOe1847Kx4Lx99osotpd02SfAwfq9JwMzdZADPS9Craw6q3tmHCC4mg5sQm1QSOJ6EVCmIYJWxIVFDXKwelavSxxeHDApcitiLa6fyOt/YH46D81ZTRN/Ne4IoZQ7hYdfG36kZgeNWH+2OwkWDD+Cn1Qo2d9lAZUrfvQSK/K7j+GYxfx3td2nn5GoH5Iv7PRD80cRDa7tTIKGBemTEDf/ABtoNxbk3h2Fnbea4i1zUI79IQsSQG+gvaNhsMcHMYpAMIKOzAMpKdHRChozT6YxFEI+jFabNZu+SkXpD8TBi_2uOZaM7q299+cxjw1v7TXqZstxcVUMVp+qmgzN5Nsi8FGUcJsrQcj8yyQxUgwkQgBIq8Y+Bdojfs543xLv3o3SFXMieTJXZVdzq+C6rGXeJGJF7Csa8ZPVafMDSAeGngBl1N9eEKOK6rGXY3OYXIg9GXZP65Vqmyp_P00gC+WEqGmT8q1ho22gXWXiBQE5YIAluQH0UsRcQlHzWpcDwwM0E_ov_7oUfBnYYUvzyf2sorQxkgQDwmXBZZoJ8zpm8g_K+RQ56LzEhkmdagR7LLUbKWeSz2qvHqTq_qRaWOx+BDbaL_ApeAbAMtx_0yhDdZmC80t_Vr3PeqX_vsDCIlHaVFKodIGmwjAbrgJzliuclnJH_xFPhziLETIK4XPR1ywd2BMQnKgv14FiEgSQtmxy4vKgkZ1YpprWHvcbWhfDa6e3alBFdQ69KG3gGKhi2C9keSowe5jLiJVLv_D1pDBVvQzN33D1rWPVHDACOTOHV9V_CjH2KCV7xxvgvAQppFRsY_yOl7i4K6gI0SifN_X7xHn2qKrqqnUho2Rjv5oGW7O096i+HsEoClA4rJ4Va0rQTzBKKBks5Xp84ULf0rFoINWGVGHkocaaQef1gnUjiV+ATvwBjBTBCTBv_+TffiV1rF_0ufz575QO9mrpdi65ovJwYJcvbjOG6ynz9PvcNPtmGVrQ6HhFXfKw5RNvAE3+8fLBKfu25_o2EBnzxzHJb5lCc9S4Su6NYWH9dNZr+2Gtgk3d3+ODTb7QaRJNwIttxvw3p5lR0glV+YGCqaffqRsY8ruWo8WoyevLH50zyLS5SvYkBK9BoC_gYqezaIDUOyIbYQalpNi0iTFIrDyovFfnpp+TVtDCgE4S_wkXlSvxMRJOKqDdYdw+XcOBkXB8T5nP27HSUCrl8HD371c0LXseotGZG83lt0NJ+som1BdgzAnRGlHK_N4LQIBEw4grBFVXJONKoY4z4VD9Epy3OM_fzK5e1FDwL8DhAjJ2oUwYsbViI0XNSCNIQ0s0HhqpEgTqQim5X5BAtMzInaswI1MyLgV4Y_H6XzzPMfHjqMb0HLypmPsC0D86yz629MAw0cdq4VlNgn+ZMlVHHNn58OHREugMPYVP9FIUJ2afngncQkHa3rQ4nRTrUgMkAJN42J95DLBhiMKxyohdhpQS+5DV1hj8ztK_Fkv8dJxG1B78P9oYLq4ujPaSvrrMUnxspMit9RFAAOlph6lcLX_utfB1fWm6cX1G4q0r9JlSf23FMZC90Bf1RUBQ9kzF2tW9KSTEsHIPNWbrsOS8t6B_V9IGJW_EknNv0gzXLAoXtuCX_TNhne0wSPtnUHch3OvDkVSmxk+GuOfb3N3X9OBzBNgWSB9QplHSQH3ucNHC8AbK5eV1lr5SNK6igupWWiafv8uFt5oHAmlNCDLYj5IHA00cwVbNFsrqhVkYpAMIKOzAMpKdHRChozT6YxFEI+jFabNZu+SkXpD8TBi_2uOZaM7q299+cxjw1v7TXqZstxcVUMVp+qmgzN5Nsi8FGUcJsrQcj8yyQxUgwkQgBIq8Y+Bdojfs543xLv3o3SFXMieTJXZVdzq+C6rGXeJGJF7Csa8ZPVafMDSAeGngBl1N9eEKOK6rGXY3OYXIg9GXZP65Vqmyp_P00gC+WEqGmT8q1ho22gXWXiBQE5YIAluQH0UsRcQlHzWpcDwwM0E_ov_7oUfBnYYUvzyf2sorQxkgQDwmXBZZoJ8zpm8g_K+RQ56LzEhkmdagR7LLUbKWeSz2qvHqTq_qRaWOx+BDbaL_ApeAbAMtx_0yhDdZmC80t_Vr3PeqX_vsDCIlHaVFKodIGmwjAbrgJzliuclnJH_xFPhziLETIK4XPR1ywd2BMQnKgv14FiEgSQtmxy4vKgkZ1YpprWHvcbWhfDa6e3alBFdQ69KG3gGKhi2C9keSowe5jLiJVLv_D1pDBVvQzN33D1rWPVHDACOTOHV9V_CjH2KCV7xxvgvAQppFRsY_yOl7i4K6gI0SifN_X7xHn2qKrqqnUho2Rjv5oGW7O096i+HsEoClA4rJ4Va0rQTzBKKBks5Xp84ULf0rFoINWGVGHkocaaQef1gnUjiV+ATvwBjBTBCTBv_+TffiV1rF_0ufz575QO9mrpdi65ovJwYJcvbjOG6ynz9PvcNPtmGVrQ6HhFXfKw5RNvAE3+8fLBKfu25_o2EBnzxzHJb5lCc9S4Su6NYWH9dNZr+2Gtgk3d3+ODTb7QaRJNwIttxvw3p5lR0glV+YGCqaffqRsY8ruWo8WoyevLH50zyLS5SvYkBK9BoC_gYqezaIDUOyIbYQalpNi0iTFIrDyovFfnpp+TVtDCgE4S_wkXlSvxMRJOKqDdYdw+XcOBkXB8T5nP27HSUCrl8HD371c0LXseotGZG83lt0NJ+som1BdgzAnRGlHK_N4LQIBEw4grBFVXJONKoY4z4VD9Epy3OM_fzK5e1FDwL8DhAjJ2oUwYsbViI0XNSCNIQ0s0HhqpEgTqQim5X5BAtMzInaswI1MyLgV4Y_H6XzzPMfHjqMb0HLypmPsC0D86yz629MAw0cdq4VlNgn+ZMlVHHNn58OHREugMPYVP9FIUJ2afngncQkHa3rQ4nRTrUgMkAJN42J95DLBhiMKxyohdhpQS+5DV1hj8ztK_Fkv8dJxG1B78P9oYLq4ujPaSvrrMUnxspMit9RFAAOlph6lcLX_utfB1fWm6cX1G4q0r9JlSf23FMZC90Bf1RUBQ9kzF2tW9KSTEsHIPNWbrsOS8t6B_V9IGJW_EknNv0gzXLAoXtuCX_TNhne0wSPtnUHch3OvDkVSmxk+GuOfb3N3X9OBzBNgWSB9QplHSQH3ucNHC8AbK5eV1lr5SNK6igupWWiafv8uFt5oHAmlNCDLYj5IHA00cwVbNFsrqhVkYpAMIKOzAMpKdHRChozT6YxFEI+jFabNZu+SkXpD8TBi_2uOZaM7q299+cxjw1v7TXqZstxcVUMVp+qmgzN5Nsi8FGUcJsrQcj8yyQxUgwkQgBIq8Y+Bdojfs543xLv3o3SFXMieTJXZVdzq+C6rGXeJGJF7Csa8ZPVafMDSAeGngBl1N9eEKOK6rGXY3OYXIg9GXZP65Vqmyp_P00gC+WEqGmT8q1ho22gXWXiBQE5YIAluQH0UsRcQlHzWpcDwwM0E_ov_7oUfBnYYUvzyf2sorQxkgQDwmXBZZoJ8zpm8g_K+RQ56LzEhkmdagR7LLUbKWeSz2qvHqTq_qRaWOx+BDbaL_ApeAbAMtx_0yhDdZmC80t_Vr3PeqX_vsDCIlHaVFKodIGmwjAbrgJzliuclnJH_xFPhziLETIK4XPR1ywd2BMQnKgv14FiEgSQtmxy4vKgkZ1YpprWHvcbWhfDa6e3alBFdQ69KG3gGKhi2C9keSowe5jLiJVLv_D1pDBVvQzN33D1rWPVHDACOTOHV9V_CjH2KCV7xxvgvAQppFRsY_yOl7i4K6gI0SifN_X7xHn2qKrqqnUho2Rjv5oGW7O096i+HsEoClA4rJ4Va0rQTzBKKBks5Xp84ULf0rFoINWGVGHkocaaQef1gnUjiV+ATvwBjBTBCTBv_+TffiV1rF_0ufz575QO9mrpdi65ovJwYJcvbjOG6ynz9PvcNPtmGVrQ6HhFXfKw5RNvAE3+8fLBKfu25_o2EBnzxzHJb5lCc9S4Su6NYWH9dNZr+2Gtgk3d3+ODTb7QaRJNwIttxvw3p5lR0glV+YGCqaffqRsY8ruWo8WoyevLH50zyLS5SvYkBK9BoC_gYqezaIDUOyIbYQalpNi0iTFIrDyovFfnpp+TVtDCgE4S_wkXlSvxMRJOKqDdYdw+XcOBkXB8T5nP27HSUCrl8HD371c0LXseotGZG83lt0NJ+som1BdgzAnRGlHK_N4LQIBEw4grBFVXJONKoY4z4VD9Epy3OM_fzK5e1FDwL8DhAjJ2oUwYsbViI0XNSCNIQ0s0HhqpEgTqQim5X5BAtMzInaswI1MyLgV4Y_H6XzzPMfHjqMb0HLypmPsC0D86yz629MAw0cdq4VlNgn+ZMlVHHNn58OHREugMPYVP9FIUJ2afngncQkHa3rQ4nRTrUgMkAJN42J95DLBhiMKxyohdhpQS+5DV1hj8ztK_Fkv8dJxG1B78P9oYLq4ujPaSvrrMUnxspMit9RFAAOlph6lcLX_utfB1fWm6cX1G4q0r9JlSf23FMZC90Bf1RUBQ9kzF2tW9KSTEsHIPNWbrsOS8t6B_V9IGJW_EknNv0gzXLAoXtuCX_TNhne0wSPtnUHch3OvDkVSmxk+GuOfb3N3X9OBzBNgWSB9QplHSQH3ucNHC8AbK5eV1lr5SNK6igupWWiafv8uFt5oHAmlNCDLYj5IHA00cwVbNFsrqhVkYpAMIKOzAMpKdHRChozT6YxFEI+jFabNZu+SkXpD8TBi_2uOZaM7q299+cxjw1v7TXqZstxcVUMVp+qmgzN5Nsi8FGUcJsrQcj8yyQxUgwkQgBIq8Y+Bdojfs543xLv3o3SFXMieTJXZVdzq+C6rGXeJGJF7Csa8ZPVafMDSAeGngBl1N9eEKOK6rGXY3OYXIg9GXZP65Vqmyp_P00gC+WEqGmT8q1ho22gXWXiBQE5YIAluQH0UsRcQlHzWpcDwwM0E_ov_7oUfBnYYUvzyf2sorQxkgQDwmXBZZoJ8zpm8g_K+RQ56LzEhkmdagR7LLUbKWeSz2qvHqTq_qRaWOx+BDbaL_ApeAbAMtx_0yhDdZmC80t_Vr3PeqX_vsDCIlHaVFKodIGmwjAbrgJzliuclnJH_xFPhziLETIK4XPR1ywd2BMQnKgv14FiEgSQtmxy4vKgkZ1YpprWHvcbWhfDa6e3alBFdQ69KG3gGKhi2C9keSowe5jLiJVLv_D1pDBVvQzN33D1rWPVHDACOTOHV9V_CjH2KCV7xxvgvAQppFRsY_yOl7i4K6gI0SifN_X7xHn2qKrqqnUho2Rjv5oGW7O096i+HsEoClA4rJ4Va0rQTzBKKBks5Xp84ULf0rFoINWGVGHkocaaQef1gnUjiV+ATvwBjBTBCTBv_+TffiV1rF_0ufz575QO9mrpdi65ovJwYJcvbjOG6ynz9PvcNPtmGVrQ6HhFXfKw5RNvAE3+8fLBKfu25_o2EBnzxzHJb5lCc9S4Su6NYWH9dNZr+2Gtgk3d3+ODTb7QaRJNwIttxvw3p5lR0glV+YGCqaffqRsY8ruWo8WoyevLH50zyLS5SvYkBK9BoC_gYqezaIDUOyIbYQalpNi0iTFIrDyovFfnpp+TVtDCgE4S_wkXlSvxMRJOKqDdYdw+XcOBkXB8T5nP27HSUCrl8HD371c0LXseotGZG83lt0NJ+som1BdgzAnRGlHK_N4LQIBEw4grBFVXJONKoY4z4VD9Epy3OM_fzK5e1FDwL8DhAjJ2oUwYsbViI0XNSCNIQ0s0HhqpEgTqQim5X5BAtMzInaswI1MyLgV4Y_H6XzzPMfHjqMb0HLypmPsC0D86yz629MAw0cdq4VlNgn+ZMlVHHNn58OHREugMPYVP9FIUJ2afngncQkHa3rQ4nRTrUgMkAJN42J95DLBhiMKxyohdhpQS+5DV1hj8ztK_Fkv8dJxG1B78P9oYLq4ujPaSvrrMUnxspMit9RFAAOlph6lcLX_utfB1fWm6cX1G4q0r9JlSf23FMZC90Bf1RUBQ9kzF2tW9KSTEsHIPNWbrsOS8t6B_V9IGJW_EknNv0gzXLAoXtuCX_TNhne0wSPtnUHch3OvDkVSmxk+GuOfb3N3X9OBzBNgWSB9QplHSQH3ucNHC8AbK5eV1lr5SNK6igupWWiafv8uFt5oHAmlNCDLYj5IHA00cwVbNFsrqhVkYpامو"
}

# 2. بناء الـ الهيدرز الموثقة والمطابقة لمعالج وسيرفر الآيفون 7 النظيف تماماً
IPHONE7_HEADERS = {
    "Host": "aws.api.snapchat.com",
    "Accept": "*/*",
    "Accept-Language": "ar-AE;q=1",
    "Content-Type": "application/x-protobuf",
    "X-Snapchat-Client-Auth-Token": IPHONE7_CLEAN_POOL["access_token"],
    "X-Snapchat-UUID": IPHONE7_CLEAN_POOL["device_uuid"],
    "X-Snap-Access-Token": IPHONE7_CLEAN_POOL["access_token"],
    # الـ User-Agent الحقيقي الخاص بنسخة الآيفون 7 ونظام 15.8.6 المستخرج من بيئتك
    "User-Agent": "Snapchat/12.80.0.35 (iPhone9,3; iOS 15.8.6; FastProxy)",
    "X-Snapshat-OS": "1",
    "X-Snapchat-App-Version": "12.80.0.35",
    "X-Snapchat-OS-Version": "15.8.6",
    "X-Snapchat-Device-Model": "iPhone9,3",
    "x-snapchat-att-token": IPHONE7_CLEAN_POOL["att_token"],
    "x-snapchat-argos-strict-enforcement": "true"
}

@app.route('/proxy_login', methods=['POST'])
def proxy_login():
    start_time = time.time()
    input_json = request.get_json() or {}
    username = input_json.get("username", "")
    
    print(f"\n[+] Injecting iPhone 7 Pure Spoofing Engine for User: {username}")
    print(f"    Target Hardware Model -> iPhone9,3 (iOS 15.8.6)")
    
    response_package = {
        "status": "success",
        "timestamp": int(time.time()),
        "processing_ms": int((time.time() - start_time) * 1000),
        "headers_snapshot": IPHONE7_HEADERS,
        "user_id": IPHONE7_CLEAN_POOL["user_id"],
        "device_uuid": IPHONE7_CLEAN_POOL["device_uuid"],
        "access_token": IPHONE7_CLEAN_POOL["access_token"],
        "access_token_alt": IPHONE7_CLEAN_POOL["access_token_alt"],
        "att_token": IPHONE7_CLEAN_POOL["att_token"],
        "protobuf_base64": IPHONE7_CLEAN_POOL["protobuf_base64_payload"]
    }
    
    return jsonify(response_package), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, threaded=True)
