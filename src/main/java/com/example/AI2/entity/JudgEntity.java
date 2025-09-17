package com.example.AI2.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Data
@Table(name = "hubdata0828")
public class JudgEntity {
    @Id
    String doc_id; //문서id
    @Column
    String doc_class; //문서 분류
    @Column
    String casenames; //사건명
    @Column
    String normalized_court; //표준화된 법원명
    @Column
    String casetype; //사건종류
    @Lob
    @Column
    String sentences; //판결문 전문
    @Column
    String announce_date; //선고일
}
