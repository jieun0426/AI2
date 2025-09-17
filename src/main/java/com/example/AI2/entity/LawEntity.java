package com.example.AI2.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Data
@Table(name = "data3")
public class LawEntity {
    @Id
    Long num;
    @Column
    String statute_name;
    @Column
    String effective_date;
    @Column
    String proclamation_date;
    @Column
    String statute_type;
    @Column
    String statute_abbrv;
    @Column
    String statute_category;
    @Column
    @Lob
    String sentences;
    @Column
    Long data_class;
}
