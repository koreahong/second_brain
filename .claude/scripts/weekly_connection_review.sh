#!/bin/bash

# Weekly Connection Review Script
# 매주 실행하여 연결성 품질을 확인합니다

VAULT_DIR="/Users/qraft_hongjinyoung/Second-Brain"
SCRIPT_DIR="$VAULT_DIR/.claude/scripts"
REPORT_DIR="$VAULT_DIR/.claude/reports"

mkdir -p "$REPORT_DIR"

echo "=================================================================================================="
echo "📊 주간 연결성 품질 리뷰"
echo "=================================================================================================="
echo ""
echo "실행 시간: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 연결성 분석
echo "1️⃣  연결성 분석 중..."
python3 "$SCRIPT_DIR/analyze_connections.py" > "$REPORT_DIR/connection_analysis_$(date '+%Y%m%d').txt"

# 2. 연결 제안 생성
echo "2️⃣  연결 제안 생성 중..."
python3 "$SCRIPT_DIR/suggest_connections.py" > "$REPORT_DIR/connection_suggestions_$(date '+%Y%m%d').txt"

# 3. 요약 리포트
echo ""
echo "=================================================================================================="
echo "✅ 완료!"
echo "=================================================================================================="
echo ""
echo "📁 리포트 저장 위치:"
echo "   - 연결성 분석: $REPORT_DIR/connection_analysis_$(date '+%Y%m%d').txt"
echo "   - 연결 제안: $REPORT_DIR/connection_suggestions_$(date '+%Y%m%d').txt"
echo "   - JSON 데이터: /tmp/connection_analysis.json"
echo "   - JSON 제안: /tmp/connection_suggestions.json"
echo ""
echo "💡 다음 단계:"
echo "   1. 리포트 확인"
echo "   2. Orphan 노트 중 5개 선택하여 연결 추가"
echo "   3. Weekly reflection에 프로젝트 링크 추가"
echo ""
