---
title: trigger + function 연동
type: resource
---

CREATE OR REPLACE FUNCTION set_dash_purchase_master_seq()

RETURNS TRIGGER AS $$

BEGIN

NEW.pk_seq := NEW.campaign_id || ':' || NEW.cus_cd || ':' || COALESCE(NEW.rep_nm, '') || ':' || COALESCE(NEW.item_nm,'') || ':' || COALESCE(NEW.purpose1, '');

RETURN NEW;

END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_dash_purchase_master_seq

BEFORE INSERT ON aivelabs_sv.dash_purchase_master

FOR EACH ROW

EXECUTE FUNCTION set_dash_purchase_master_seq();

DROP TRIGGER IF EXISTS trigger_dash_purchase_master_seq ON aivelabs_sv.dash_purchase_master;

DROP FUNCTION IF EXISTS set_dash_purchase_master_seq();

```plain text

위에서 new.컬럼으로 가져오는 부분에서 pk_seq 컬럼의 값을 생성하는
컬럼들 중 어느 한개라도 null이면 pk_seq값이 null로 들어간다.
따라서, pk_seq를 pk로 사용하는 경우에는 구성하는 컬럼들이
null이면 기본값이 들어갈 수 있게 설정을 해줘야 한다.
```