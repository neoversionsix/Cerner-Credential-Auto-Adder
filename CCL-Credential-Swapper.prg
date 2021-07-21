
update into credential c
set c.prsnl_id = 
, c.updt_dt_tm = cnvtdatetime(curdate,curtime3)
, c.updt_id = reqinfo->updt_id
, c.updt_cnt = c.updt_cnt + 1
where c.credential_id = "&C2&";",""